from phe import paillier
import numpy as np
import requests

URL = "http://localhost:8000"
PRECISION = 2**(-16)
EXPONENT = -8


def query_pred(vector: list, keys: tuple = None):
    if keys is None:
        pubkey, privkey = paillier.generate_paillier_keypair()
    else:
        pubkey, privkey = keys
    enc_vector = [pubkey.encrypt(x, precision=PRECISION)
                  .ciphertext() for x in vector]
    # print(enc_vector)
    r = requests.post(URL+"/prediction",
                      json={"pub_key_n": pubkey.n,
                            "enc_feature_vector": enc_vector})
    if r.status_code != 200:
        print("Error while requesting_ {}".format(r.status_code))
    # print([pubkey.encrypt(x).ciphertext() for x in vector])
    y_enc = r.json()['enc_prediction']
    encrypted = paillier.EncryptedNumber(pubkey, y_enc, EXPONENT)
    y = privkey.decrypt(encrypted)
    # print("Returning", y)
    return y


def main_weight_by_weight():
    keys = paillier.generate_paillier_keypair()
    weights = []
    print("Attacking bias")
    bias = query_pred([0]*10, keys)

    for i in range(10):
        print("Attacking weight {}".format(i), end="\r")
        vector = np.zeros(10)
        vector[i] = 1
        y = query_pred(vector, keys) - bias
        weights.append(y)
    print("\nWeights: {}\nbias: {}".format(weights, bias))


def main_linear_equation():
    keys = paillier.generate_paillier_keypair()
    X, y = [], []
    for i in range(11):
        print("Iteration", i)
        vector = np.random.random_sample(10)
        y.append(query_pred(vector, keys))
        X.append(np.append(vector, 1))
    X = np.array(X)
    y = np.array(y)
    print(X.shape, y.shape)
    weights = np.linalg.solve(X, y)
    print(weights)


if __name__ == "__main__":
    main_linear_equation()
