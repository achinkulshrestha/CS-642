'''
Created on Nov 26, 2014

@author: Achin
'''
from subprocess import Popen, PIPE
import sys
from operator import pos
keyfile=""
hexCiphertext = ""
dic=[]
def convertStrToList(str1):
    cipher = []
    i=0
    while i<32:
        cipher.append(str1[i]+str1[i+1])
        i +=2
    print cipher
    return cipher
def main():
    if(len(sys.argv) > 2):
        keyfile = sys.argv[1]
    if(len(sys.argv[2]) > 1):
        f = open( sys.argv[2], 'r')
        hexCiphertext = f.read()
    binaryCipherText = hexCiphertext.decode("hex")
    iv = []
    interB =[]
    for lenIV in range(0,16):
        iv.append('{:02x}'.format(lenIV))
    for iBy in range(0,16):
        interB.append('{:02x}'.format(iBy))

    firstByte = hexCiphertext[32:64]
    cipherList = convertStrToList(firstByte)
    print len(cipherList)

    tag = hexCiphertext[64:128]
    pos = 15
    val = 0
    while pos >= 0:
        for i in range(0,255):
            iv[pos] = '{:02x}'.format(i)
            firstBlock = ''.join(iv)
            print "The IV is %s" % firstBlock
            finalText = firstBlock+firstByte+tag
            #finalText = struct.pack('<16B16B32B',firstBlock,first,tag)
            print finalText
            proc = Popen(["baddecrypt.py",keyfile,finalText],stdout=PIPE, stderr=PIPE,shell=True)
            output = proc.communicate()[0]
            #print proc
            print output
            if(output.find("Tag doesn't verify!\n") != -1):
                print "intermediate Byte "
                iByte =  val ^ i
                print iByte
                interB[pos] = iByte
                dic.append('{:02x}'.format(int(cipherList[pos],16) ^ iByte))
                break
        curPos = pos
        while curPos <= 15:
            iv[curPos] = '{:02x}'.format(int(str(interB[curPos]),16) ^ (val+1))
            curPos += 1
        pos -= 1
        val +=  1
    print dic
    reversedDic = ''.join(reversed(dic))
    print reversedDic.decode("hex")


if __name__ == '__main__':
    main()
