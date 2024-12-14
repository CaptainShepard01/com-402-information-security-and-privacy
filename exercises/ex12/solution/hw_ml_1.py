from phe import paillier
import requests

URL = "http://localhost:8000"
N = 2048
g = N + 1
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
    print("Returning", y)
    return y


def main():
    assert 2**(-16) > abs(query_pred([0.48555949, 0.29289251, 0.63463107,
                                      0.41933057, 0.78672205, 0.58910837,
                                      0.00739207, 0.31390802, 0.37037496,
                                      0.3375726]) - 0.44812144746653826)


if __name__ == "__main__":
    main()
