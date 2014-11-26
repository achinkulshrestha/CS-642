#!/usr/bin/python
# CS 642 University of Wisconsin
#
# WARNING:
# Do not use this encryption functionality, it has security vulnerabilities!
#
# Your job is to find and understand the problems
#
# usage: badencrypt.py keyfile message
#

import sys
import os
import Crypto.Cipher.AES
#from Crypto.Random import get_random_bytes
import hmac
import hashlib
import base64
import struct
import math

f = open( sys.argv[1], 'r')
key1 = f.readline()
key1 = key1[:32].decode("hex")
key2 = f.readline()
key2 = key2[:32].decode("hex")
f.close()

message = sys.argv[2]

# We set pad byte to be number of padding bytes needed minus one. So, if we need
# to pad by 5, we use 4 4 4 4 4. Decryption will read off last byte, and then
# check the padding bytes indicated by that first byte. 
padbyte = 16 - (len(message) + 1) % 16
padded_message = message + struct.pack('<' + 'B'*int(padbyte+1),*([padbyte]*int(padbyte+1))) 

iv = os.urandom(16)
cipher = Crypto.Cipher.AES.new(key1, Crypto.Cipher.AES.MODE_CBC, IV=iv )
ciphertext = str(iv) + cipher.encrypt( padded_message )
tag = hmac.new(key2, ciphertext, hashlib.sha256).digest()

print (ciphertext + tag).encode("hex")

