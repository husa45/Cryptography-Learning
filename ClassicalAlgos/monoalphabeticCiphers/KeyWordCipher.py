#This is a simple monoalphabetic substitution cipher ,where the key is placed at 
#beggining of the alphabet ,then every character duplicated is excluded from the alphabet
#then it becomes a simple monoalphabetic cipher
class keyword_cipher(object):
    
    def __init__(self, abc, keyword):
        self.seen=set({})
        self.key=""
        self.alphabet=abc
        print(abc,keyword)
        for char in keyword:
            if char.lower() not in self.seen:
                self.key+=char
                self.seen.add(char)
        for char in abc:
            if char not in self.seen:
                self.key+=char
                self.seen.add(char)
        print(self.key)
    def encode(self, plain):
        print(plain)
        print(plain)
        result=""
        for char in plain:
            if char in self.seen:
                index=self.alphabet.index(char)
                result+=self.key[index]
            else:
                result+=char
        return result 
    def decode(self, ciphered):
        print(ciphered)
        result=""
        for char in ciphered:
            if char in self.seen:
                index=self.key.index(char)
                result+=self.alphabet[index]
            else:
                result+=char
        return result