import os.path
import string
import random
from binascii import hexlify
import sys
from logging import exception


class VernamAlgo:
    def __int__(self):
        self.key=None#''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits+string.ascii_lowercase) for _ in range(N))
    def encrypt(self,plainText:'bytes')->'bytes':
        if not os.path.exists("KEY.txt"):
            self.key=bytes(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(len(plainText))),encoding="utf-8")
            with open("KEY.txt","wb") as outo:
                outo.write(self.key)
        else:
            with open("KEY.txt","rb") as ino:
                self.key=ino.read()
        if len(self.key)!=len(plainText):
            self.key = bytes(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(len(plainText))),encoding="utf-8")
            with open("KEY.txt", "wb") as outo:
                outo.write(self.key)
        result=bytearray()
        for i in range(0,len(self.key)):
            result.append(self.key[i]^plainText[i])
        return bytes(result)
    def decrypt(self,cipherText:'bytes')->'bytes':
        if not os.path.exists("KEY.txt"):
            self.key = bytes(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(len(cipherText))))
            with open("KEY.txt", "wb") as outo:
                outo.write(self.key)
        else:
            with open("KEY.txt", "rb") as ino:
                self.key = ino.read()
        if len(self.key)!=len(cipherText):
            self.key = bytes(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(len(cipherText))),encoding="utf-8")
            with open("KEY.txt", "wb") as outo:
                outo.write(self.key)
        result=bytearray()
        for i in range(0,len(self.key)):
            result.append(self.key[i]^cipherText[i])
        return bytes(result)
def main():
    print("Choose what you want to do \n1.Encryption (enter 1) 2.Decryption (Enter 2)\nThe key will be randomly generated ,and will be of as length as the input for perfect secrecy (It is stored in a file KEY.txt in the current directory)")
    print("This is only for Educational purposes ,this should not be used in real settings ,Also the key must be distributed with a proper method(like public key cryptography) not stored directly in a file")
    choice=input("Choice : \n").strip()
    obj=VernamAlgo()
    if choice=="1":
        result=obj.encrypt(bytes(input("Enter data to encrypt: \n"),encoding="utf-8"))
        print(hexlify(result))
    elif choice=="2":
        result = obj.decrypt(bytes(input("Enter data to decrypt: \n"),encoding="utf-8"))
        print(hexlify(result))
    else:
        raise SystemExit("You should choose either 1 or 2")
if __name__=="__main__":
    main()