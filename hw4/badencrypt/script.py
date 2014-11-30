'''
Created on Nov 26, 2014

@author: Achin
'''
from subprocess import Popen, PIPE
import sys
keyfile=""
hexCiphertext = ""

def main():
    if(len(sys.argv) > 2):
        keyfile = sys.argv[1]
    if(len(sys.argv[2]) > 1):
        f = open( sys.argv[2], 'r')
        hexCiphertext = f.read()

    proc = Popen(["baddecrypt.py",keyfile,hexCiphertext],stdout=PIPE,shell = True)
    output = proc.communicate()[0]
    print output

if __name__ == '__main__':
    main()
