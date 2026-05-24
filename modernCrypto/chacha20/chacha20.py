from sys import int_info
from Crypto.Random import get_random_bytes
def ROL(number,count):
    return (number <<count)|(number >>(32-count))
class chacha20:
    def __init__(self):
        self.key=get_random_bytes(256)
        self.nonce=get_random_bytes(256)
        self.CONSTANT=b"expand 32-byte k"
        self.keystreams=[]
    def Quarter(self,a,b,c,d)->'list':
        a=(a+b)&0xffffffff;d^=a;ROL(d,16)
        c=(c+d)&0xffffffff;b^=c;ROL(b,12)
        a = (a + b) & 0xffffffff;d^=a;ROL(d,8)
        c = (a + d) & 0xffffffff;b^=c;ROL(b,7)
        return [a,b,c,d]
    def __prepareInitialState(self,counter)->'None':
        #concatenate to one byte string , then convert into 4X4 32bit little endian components:
        state_string=self.CONSTANT+self.key+counter+self.nonce
        words=[ int.from_bytes(state_string[i:i+4],"little") for i in range(0,len(state_string),4)]
        initialState=[ words[i:i+4]    for i in range(0,16,4)]
        return initialState
    def generateKeyStream(self,initialState,originalState)->'bytearray':
        #generate modified state:
        for i in range(0,10):
            #first round for columns:
            initialState[0][0],initialState[1][0],initialState[2][0],initialState[3][0]=self.Quarter(initialState[0][0],initialState[1][0],initialState[2][0],initialState[3][0])
            initialState[0][1], initialState[1][1], initialState[2][1], initialState[3][1] = self.Quarter(initialState[0][1],initialState[1][1],initialState[2][1],initialState[3][1])
            initialState[0][2], initialState[1][2], initialState[2][2], initialState[3][2] = self.Quarter(initialState[0][2],initialState[1][2],initialState[2][2],initialState[3][2])
            initialState[0][3], initialState[1][3], initialState[2][3], initialState[3][3] = self.Quarter(initialState[0][3],initialState[1][3],initialState[2][3],initialState[3][3])
            #second round for diagonals:
            initialState[0][0], initialState[1][1], initialState[2][2], initialState[3][3] = self.Quarter(initialState[0][0],initialState[1][1],initialState[2][2],initialState[3][3])
            initialState[0][3], initialState[1][2], initialState[2][1], initialState[3][0] = self.Quarter(initialState[0][3],initialState[1][2],initialState[2][1],initialState[3][0])
            initialState[0][1], initialState[1][2], initialState[2][3], initialState[3][0] = self.Quarter(initialState[0][1],initialState[1][2],initialState[2][3],initialState[3][0])
            initialState[0][3], initialState[1][0], initialState[2][1], initialState[3][2] = self.Quarter(initialState[0][3],initialState[1][0], initialState[2][1],initialState[3][2])
        #Now the modified state is ready:
        modifiedState=initialState.copy()
        #preparing the keystream:
        #1.flattening the modifiedState:
        temp=[]
        for row in modifiedState:
            temp.extend(row)
        modifiedState=temp
        #2.flattening the original state:
        temp=[]
        for row in originalState:
            temp.extend(row)
        originalState=temp
        #preparing the keystream:
        keyStream = bytearray()
        for i in range(0,16):
            dword=(originalState[i]+modifiedState[i])&0xffffffff
            keyStream.extend(dword.to_bytes(4,"little"))
        return keyStream
    def chacha20Main(self,counter)->'bytearray':
            #for every 64 byte block , generate a key stream
            counter=int.to_bytes(counter,4,"little")
            #get the initial state for the current block
            initialState=self.__prepareInitialState(counter)
            #copy the initialState
            initialStateCopy=initialState.copy()
            #generate the keystream:
            return self.generateKeyStream(initialStateCopy,initialState)
    def chach20Encrypt(self,plainData:'bytes')->'bytes':
        encrypted = []
        for i in range(0, len(plainData), 64):
            keyStream=self.chacha20Main((0 if i==0 else i//64))
            self.keystreams.append(list(keyStream))
            block=bytearray(plainData[i:i+64])
            for u in range(0,len(block)):
                block[u]=block[u]^keyStream[u]
            encrypted.extend(block)

        return bytes(encrypted)
    def chach20Decrypt(self,cipherData:'bytes')->'bytes':
        decrypted=[]
        for i in range(0, len(cipherData), 64):
            counter=(0 if i==0 else i//64)
            block=bytearray(cipherData[i:i+64])
            for u in range(0,len(block)):
                block[u]=block[u]^self.keystreams[counter][u]
            decrypted.extend(block)
        return bytes(decrypted)
def main():
    pass
if __name__=="__main__":
    main()