'''
Created on Nov 26, 2014

@author: Achin
'''

#!/usr/bin/python
# CS 642 University of Wisconsin
#
# WARNING:
# Do not use this encryption functionality, it has security vulnerabilities!
#
# Your job is to find and understand the problems
#
# usage: baddecrypt.py keyfile ciphertext
#

import sys
import Crypto.Cipher.AES
#from Crypto.Random import get_random_bytes
import hmac
import hashlib
import base64
import struct


def main():
    f = open( sys.argv[1], 'r' )
    key1 = f.readline()
    key1 = key1[:32].decode("hex")
    key2 = f.readline()
    key2 = key2[:32].decode("hex")
    f.close()
    
    # Grab ciphertext from first argument
    cipherTextinHex = sys.argv[2]
    ciphertextWithTag = (sys.argv[2]).decode("hex")
    
    if len(ciphertextWithTag) < 16+16+32:
      print "Ciphertext is too short!"
      sys.exit(0) 
    
    ciphertext = ciphertextWithTag[:len(ciphertextWithTag)-32]
    #print "CipherTextwithoutTag" 
    #print ciphertext.encode("hex")  
    tag = ciphertextWithTag[len(ciphertextWithTag)-32:]   
    iv = ciphertextWithTag[:16]
    #print "Initialization Vector" 
    #print iv.encode("hex")  
    
    cipher = Crypto.Cipher.AES.new(key1, Crypto.Cipher.AES.MODE_CBC, IV=iv )
    #print "cipherblock"
    #print ciphertext[16:].encode("hex")
    plaintextWithPad = cipher.decrypt( ciphertext[16:] )
    #print "PlainText With Pad" 
    #print plaintextWithPad.encode("hex")  
    
    l = len(plaintextWithPad)
    padbyte = struct.unpack("<B" , plaintextWithPad[l-1])[0]
    #print "Padbyte"
    #print padbyte
    if int(padbyte) > l:
      print "Padding error!"
      sys.exit(0)
    
    padbytes = struct.unpack('<' + 'B'*(int(padbyte)+1), plaintextWithPad[l-int(padbyte)-1:l] )
    # Check padding bytes
    for p in padbytes:
      if p != padbyte:
        print "Padding error!"
        sys.exit(0)
    
    # Check HMAC
    tagCheck = hmac.new(key2, ciphertext, hashlib.sha256).digest()
    if tagCheck != tag:
        print "Tag doesn't verify!"
        sys.exit(0)
    
    plaintext = plaintextWithPad[:l-int(padbyte)-1]
    # TODO: Insert routines to process recovered plaintext
    
    print "Message received! %s " % plaintext
    


if __name__ == '__main__':
    main()