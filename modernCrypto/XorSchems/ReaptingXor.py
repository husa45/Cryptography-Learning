def XorRepatingEncrypt(plaintext:'str')->'bytes':
    result=bytearray()
    key=b"FUCK"
    keyLen=len(key)
    for i  in range(0,len(plaintext)):
        result.append((plaintext[i])^(key[i%keyLen]))
    return bytes(result)
def XorReapeatingDecrypt(cipherText:'str')->'bytes':
    result = bytearray()
    key = b"FUCK"
    keyLen = len(key)
    for i in range(0, len(cipherText)):
        result.append((cipherText[i]) ^ (key[i % keyLen]))
    return bytes(result)
def main():
    plaintext=b"This is the best day in the year"
    cipherText=XorRepatingEncrypt(plaintext)
    print("The encrpyted data: ",cipherText,sep="\n")
    print(XorReapeatingDecrypt(cipherText))
if __name__=="__main__":
    main()