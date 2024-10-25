import os
import hashlib
import socket
import threading
import socketserver
import struct
import time
import threading

from base64 import b64encode, b64decode
from pwn import *

def md5(bytestring):
    return hashlib.md5(bytestring).digest()
def sha(bytestring):
    return hashlib.sha1(bytestring).digest()
def blake(bytestring):
    return hashlib.blake2b(bytestring).digest()
def scrypt(bytestring):
    l = int(len(bytestring) / 2)
    salt = bytestring[:l]
    p = bytestring[l:]
    return hashlib.scrypt(p, salt=salt, n=2**16, r=8, p=1, maxmem=67111936)

def xor(s1, s2):
    return b''.join([bytes([s1[i] ^ s2[i % len(s2)]]) for i in range(len(s1))])

def main():
    io = remote('127.0.0.1', 1337)
    print(io.recv(1000))
    ans_array = bytearray()
    while True:
        buf = io.recv(1)
        if buf:
            ans_array.extend(buf)
        if buf == b'!':
            break

    password_hash_base64 = ans_array[ans_array.find(b"b'") + 2: ans_array.find(b"'\n")]
    password_hash = b64decode(password_hash_base64)
    print('password:', password_hash)
    method_bytes = ans_array[
        ans_array.find(b'used:\n') + 6 : ans_array.find(b'\nYour')
    ]
    methods = method_bytes.split(b'\n')
    methods = [bytes(x.strip(b'- ')).decode() for x in methods]
    print(methods)

    # reverse the hash calculation
    in_salt = password_hash[:64]
    in_hash = password_hash[64:]
    for pos, neg in zip(methods, methods[::-1]):
        '''
            interim_salt = xor(interim_salt, hash_rounds[-1-i](interim_hash))
            interim_hash = xor(interim_hash, hash_rounds[i](interim_salt))
        '''
        in_hash = xor(in_hash, eval("{}(in_salt)".format(neg)))
        in_salt = xor(in_salt, eval("{}(in_hash)".format(pos)))
    print(in_hash, in_salt)

    # extract the password between '{' and '}'
    in_hash = in_hash[-20:]
    password = in_hash[(in_hash.find(b'{')):(in_hash.find(b'}')+1)]

    print(password)
    io.send(password)
    io.interactive()

if __name__ == '__main__':
    main()