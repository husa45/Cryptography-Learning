def extendKey(text,key):
        currLen=0
        keyLen=len(key)
        extendedKey=""
        for i in range(0,len(text),keyLen):
            extendedKey+=key
            currLen+=len(key)
        if currLen<=len(text):
            extendedKey+=key[:len(key)-currLen]
        else:
            extendedKey=key[:-1*(currLen-len(text))]
        return extendedKey
            
class VigenereCipher(object):
    def __init__(self, key, alphabet):
        self.alphabet=alphabet
        self.key=key
        currLen=0
        keyLen=len(key)
        for i in range(0,len(alphabet),keyLen):
            self.key+=key
            currLen+=len(key)
        if currLen<=len(alphabet):
            self.key+=key[:len(key)-currLen]
        else:
            self.key=self.key[:-1*(currLen-len(alphabet))]
    def encode(self, text):
        self.key=extendKey(text,self.key)
        cipherText=""
        for char in text:
            alphabetIndex=self.alphabet.index(char)
            newIndex=(alphabetIndex+self.key[alphabetIndex])%len(self.alphabet)
            cipherText+=self.alphabet[newIndex]
    def decode(self, text):
        pass
xc=VigenereCipher("deciptive","abcdefghijklmnopqrstuvw")