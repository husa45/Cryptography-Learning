import hashlib
import binascii

IPAD_CONSTANT=0x36
OPAD_CONSTANT=0x5c
HASH_BLOCK_LENGTH=64
class HMAC:
    """
    This class implements HMAC-sha256 as Guided by RFC 2104
    According to RFC ,the key length must be at least L (The output length in bytes ,for the cryptographic hash function used)
    And up to B (Block length of the hash function ,ie:MD5 ,sha1 ,sha256  to be 64)
        And otherwise ,will be padded by \x00
    IPAD :0x36 repeated * The block length of the Hash Function
    OPAD :0x5c repeated * The block length of the Hash Function
    """
    def __init__(self,key:'bytes') -> None:
        self.IPAD=bytes([IPAD_CONSTANT]*HASH_BLOCK_LENGTH)
        self.OPAD=bytes([OPAD_CONSTANT]*HASH_BLOCK_LENGTH)
        self.key=key+(b"\x00"*(HASH_BLOCK_LENGTH-len(key) if len(key)<HASH_BLOCK_LENGTH else 1))
        self.key1=self.__generate_keys(self.key,self.IPAD)
        self.key2=self.__generate_keys(self.key,self.OPAD)
    def __generate_keys(self,KEY,PAD):
        result=[]
        pair=zip(KEY,PAD)
        for key_byte,PAD_byte in pair:
            result.append(key_byte^PAD_byte)
        return bytes(result)
    def generate_HMAC(self,message:'bytes'):
        #round 1:
        round1_hash=hashlib.sha256(self.key1+message).digest()
        #round 2:
        MAC=hashlib.sha256(self.key2+round1_hash)
        return MAC.digest()
def main():
    #read the key from the config file
    key=b""
    with open("key.config","rb") as reader:
        key=reader.read()
    hmac_object=HMAC(key)
    MAC=binascii.hexlify(hmac_object.generate_HMAC(b"The quick brown fox jumps over the lazy dog"))
    print(f"The MAC is  {MAC}")
if __name__=="__main__":
    main()