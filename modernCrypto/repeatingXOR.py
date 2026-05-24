from binascii import *
def main():
    template=bytearray(b"crypto{}")
    length=len(template)
    f_bytes=bytearray(unhexlify("0e0b213f26041e04"))
    for i in range(0,length):
        template[i]^=f_bytes[i]
    length = len(template)
    print(template)
    encrypted=bytearray(unhexlify("0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"))
    for i in range(0,len(encrypted)):
        encrypted[i]^=template[i%length]
    print(encrypted.decode())


if __name__=="__main__":
    main()
