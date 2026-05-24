from Crypto.Random import get_random_bytes
from Crypto.SelfTest.Cipher.test_CFB import bits
from binascii import *

class TEA:

    def __init__(self):
        self.DELTA=0x9e3779b9
        self.key=int.from_bytes(get_random_bytes(16),"little") #128 bit random key
        self.key=[self.key&0xffffffff,(self.key>>32)&0xffffffff,(self.key>>64)&0xffffffff,(self.key>>96)&0xffffffff]
        self.targetLength=64
    def encrypt(self,block):
        v0,v1=block[0],block[1]
        sum,rounds=0,32
        for i in range(0,rounds):
            sum+=self.DELTA
            v0+=((v1<<4)+self.key[0]) ^(v1+sum)^((v1>>5)+self.key[1])
            v1+=((v0<<4)+self.key[2]) ^(v0+sum)^((v0>>5)+self.key[3])
            block[0]=v0
            block[1]=v1
        return block
    def decrypt(self,block):
        v0,v1=block[0],block[1]
        rounds=32
        sum=self.DELTA*rounds
        for i in range(0, rounds):
            v1 -= ((v0 << 4) + self.key[2]) ^ (v0 + sum) ^ ((v0 >> 5) + self.key[2])
            v0 -= ((v1 << 4) + self.key[0]) ^ (v1 + sum) ^ ((v1 >> 5) + self.key[1])
            block[0] = v0
            block[1] = v1
            sum-=self.DELTA
        return block
    def TEA_main(self,plainData:'bytes'):
        length=len(plainData)
        encrypted=[]
        for i in range(0,length,64):
            block=plainData[i:i+64]
            #pad the block to the desired size:
            block +=(b"0" *(64-length))
            block=int.from_bytes(block,"little")
            toPass=[0]*2
            toPass[0]=(block&0xfffffff)
            toPass[1] = ((block >> 32) & 0xfffffff)
            encrypted.extend(self.encrypt(toPass))
        return encrypted


f=TEA()
print(f.TEA_main(b"hussam aljaar"))