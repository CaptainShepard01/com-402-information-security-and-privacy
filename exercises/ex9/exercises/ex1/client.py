#!/usr/bin/env python3
import socket
import urllib3
import json
import sys
import hashlib
import random
import string
import time
import base64
from queue import Queue
from io import StringIO
import re
import requests

pkt_types = ["garbage"] * 5 + ["pwd"] * 1 + ["misleading_garbage"] * 1

MAX_PAYLOAD_SIZE = 100
MIN_PAYLOAD_SIZE = 1


misleading_garbage = [
    "cc --_ 1094.5623.4.45",
    "pwd --_ sunnY_daY",
    "cc --_ 7629.56...",
    "cc -- 7865.0924.1287.438",
    "pwd --_ stay@strong",
]
secrets = [
    "pwd --- VERYSECURE1111",
    "cc --- 8452.8214.9088.8566",
    "pwd --- UQXI5I06UX924",
]

secrets_sent = False
shipping_sent = False


def send_http(url, json):
    try:
        print("Sending", json, "to", url)
        r = requests.post(url=url, headers={"secret": json})
        if r.status_code == 200:
            answer = r.json()
            print("Successfully sent", answer["data"])
    except Exception as e:
        print(e)


def gen_rnd_string(len):
    return "".join(
        random.SystemRandom().choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        )
        for _ in range(len)
    )


def run(url):
    i = 0
    while True:
        rnd_pkt_type = random.choice(pkt_types)

        if i < 3:
            rnd_pkt_type = "pwd"  # to ease testing
            i += 1

        if rnd_pkt_type == "garbage":
            payload = gen_rnd_string(random.randint(MIN_PAYLOAD_SIZE, MAX_PAYLOAD_SIZE))
            send_http(url, payload)
        if rnd_pkt_type == "pwd":
            secret = random.choice(secrets)
            payload = gen_rnd_string(
                random.randint(MIN_PAYLOAD_SIZE, MAX_PAYLOAD_SIZE // 2)
            )
            payload2 = gen_rnd_string(
                random.randint(MIN_PAYLOAD_SIZE, MAX_PAYLOAD_SIZE // 2)
            )
            send_http(url, payload + " " + secret + " " + payload2)
        if rnd_pkt_type == "misleading_garbage":
            garbage = random.choice(misleading_garbage)
            payload = gen_rnd_string(
                random.randint(MIN_PAYLOAD_SIZE, MAX_PAYLOAD_SIZE // 2)
            )
            payload2 = gen_rnd_string(
                random.randint(MIN_PAYLOAD_SIZE, MAX_PAYLOAD_SIZE // 2)
            )
            send_http(url, payload + " " + garbage + " " + payload2)
        time.sleep(10)


if __name__ == "__main__":
    url = sys.argv[1]
    print("Client booting... (10 seconds)")
    time.sleep(10)
    run(url)
