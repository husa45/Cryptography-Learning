def extendKey(text, key):
    print(f"KEy beofre extend : {key}")
    currLen = 0
    keyLen = len(key)
    extendedKey = ""
    u = 0
    for i in range(0, len(text)):
        extendedKey += key[u]
        u += 1
        if u % len(key) == 0 and u != 0:
            u = 0
    return extendedKey


class VigenereCipher(object):
    def __init__(self, key, alphabet):
        self.alphabet = alphabet
        self.key = key

    def encode(self, text):
        key = extendKey(text, self.key)
        print(f"key {self.key}")
        print(f"Alphabet : {self.alphabet}")
        print(f"plain text  :{text}")
        cipherText = ""
        decryptedBefore = set({})
        i = 0
        for char in text:
            if char in self.alphabet:  # use a set faster
                correspondingChar = key[i]
                newIndex = (self.alphabet.index(char) + self.alphabet.index(correspondingChar)) % len(self.alphabet)
                cipherText += self.alphabet[newIndex]

            else:
                cipherText += char
            i += 1

        return cipherText

    def decode(self, text):
        key = extendKey(text, self.key)
        print(f"key {self.key}")
        print(f"Alphabet : {self.alphabet}")
        print(f"cipher text  :{text}")
        plainText = ""
        decryptedBefore = set({})
        i = 0
        for char in text:
            if char in self.alphabet:  # use a set faster
                correspondingChar = key[i]
                newIndex = (self.alphabet.index(char) - self.alphabet.index(correspondingChar)) % len(self.alphabet)
                plainText += self.alphabet[newIndex]

            else:
                plainText += char
            i += 1

        return plainText
# xc=VigenereCipher("deciptive","abcdefghijklmnopqrstuvw")


