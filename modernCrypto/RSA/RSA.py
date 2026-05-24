from math import ceil, log2

from Crypto.Util.number import bytes_to_long

from GCD import GCD
from Crypto.Util import number
from MInverse import Minverse
from random import randint
class RSA:
    def __init__(self):
        self.N:'int'=0
        self.eulersTotient:'int'=0
        self.Phi=0
        self.e=0
        self.d=0


    def choosePublicKey(self)->'int':
        for e in range(65535,self.Phi):
            if GCD(e,self.Phi)==1:
                return e
    def generatePublicKey(self):
        P=number.getPrime(2048)
        Q=number.getPrime(2048)
        self.N=P*Q
        self.Phi=(P-1)*(Q-1)
        #choosing public key:
        #such that 1<e<Phi(N) ^(gcd(e,phi(n))==1 ^gcd(e,N)==1)
        self.e=self.choosePublicKey()
    def generatePrivateKey(self):
        self.d=Minverse([self.e,self.Phi])
        if self.d==0:
            raise SystemExit("Cant derive  a private key")
    def padMessage(self,data)->'bytes':
        #where k is the length of the modulus in bytes:
        k=(self.N.bit_length()+7)//8
        #where m is the length of message in bytes:
        m=ceil(log2(bytes_to_long(data))/8)
        if m >k-11:
            return data
        #prepare the padding as follows:
        #0x0,0x2,P,0x0,Message
        #whre the length of P must be k-len(M)-3 ,len(ps)>=8
        message=bytearray(data)
        padding=bytearray()
        padding.append(0x0)
        padding.append(0x02)
        PLength=k-m-3
        for i in range(1,PLength+1):
            padding.append(randint(1,255))
        padding.append(0x0)
        padding.extend(message)
        return bytes(padding)
    def unpadMessage(self,data:'bytes'):
        startIndex=0
        for i in range(1,len(data)):
            if data[i]==0x0:
                startIndex=i+1
                break
        return data[startIndex:]
    def encryption(self,plainData:'bytes'):
        #PKCS  # v1.5:This padding is for learning purposes only ,and should not be used in reeal world implementation
        #0x00 0x02 [some random nonzero bytes] 0x0 message
        plainData:'bytes'=self.padMessage(plainData)
        dataAsNumber=number.bytes_to_long(plainData)
        return pow(dataAsNumber,self.e,self.N)
    def decryption(self,cipherData:'int')->'bytes':
        decrypted=pow(cipherData,self.d,self.N)
        #print(decrypted)
        decrypted = number.long_to_bytes(decrypted)
        decrypted=self.unpadMessage(decrypted)
        return decrypted
def test_key_sanity(rsa):
    print("[TEST] Key sanity")
    assert rsa.N > 0
    assert rsa.e > 1
    assert rsa.d > 1
    assert (rsa.e * rsa.d) % rsa.Phi == 1
    print("OK")
def test_encrypt_decrypt(rsa):
    print("[TEST] Encrypt/Decrypt identity")
    msg = b"hello world"
    c = rsa.encryption(msg)
    p = rsa.decryption(c)
    if p == msg:
        print("OK")
def test_multiple_messages(rsa):
    print("[TEST] Multiple messages")
    messages = [
        b"A",
        b"Test",
        b"RSA implementation",
        b"\x00\x01\x02\x03\x04"
    ]
    for m in messages:
        c = rsa.encryption(m)
        p = rsa.decryption(c)
        assert p == m
    print("OK")
def test_random_messages(rsa):
    print("[TEST] Random messages")
    for _ in range(10):
        length = randint(1, 64)
        m = bytes(randint(0,255) for _ in range(length))
        c = rsa.encryption(m)
        p = rsa.decryption(c)
        assert p == m
    print("OK")
def test_rsa_math(rsa):
    print("[TEST] RSA mathematical property")
    m = randint(2, rsa.N-1)
    c = pow(m, rsa.e, rsa.N)
    p = pow(c, rsa.d, rsa.N)
    assert p == m
    print("OK")

rsa=RSA()
rsa.generatePublicKey()
rsa.generatePrivateKey()

