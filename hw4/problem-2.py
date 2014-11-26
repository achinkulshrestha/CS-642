import hashlib
import sys
username = b"ristenpart,"
salt = b",134153169"
password = b""

answer = "37448ba7de7f5b4396697edaeddcd7bc840964e6ce82016915b830a91d69eb2f"

def checkSha(str1):
  print str1
  password = str1
  hashObj = hashlib.sha256(username+password+salt)
  hexDig = hashObj.hexdigest()
  if(hexDig == answer):
    print "yippie"
    print(hexDig)
    print password
    sys.exit(0)

def printBuf(buf,len):
  print buf
def makeString(buf,len):
  str1 = ''
  for e in buf:
    if(e == '\0'):
      break
    str1 += str(e)
  checkSha(str1)

def permute(curPosition, len, numberArr, buf):
  if(curPosition == len):
    makeString(buf,len)
    return
  for i in numberArr:
    #print "numberArr Value %c" % i
    #print "CurPosition is %d" %curPosition
    buf[curPosition] = i
    permute(curPosition + 1,len,numberArr, buf)


def main():
  buf =[]
  for i in range(0,100):
    buf.append('\0')
  numberArr = ['0','1','2','3','4','5','6','7','8','9']
  for len in range(1,100):
    curPosition = 0
    #print 'Length %d ' % len
    permute(curPosition,len,numberArr,buf)

if __name__ == "__main__":
  main()
