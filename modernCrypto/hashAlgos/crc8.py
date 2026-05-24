from binascii import *
def input_reflection(number,size)->'int':
    return (int(bin(number)[2:].zfill(size)[::-1],2))
class Crc8Algo:
    def __init__(self,initial_crc,generator,input_reflection:'bool',result_reflection:'bool',final_xor:'int'):
       self.crc8_lookup_table=[0]*256
       self.generator=generator
       self.initial_crc=initial_crc
       self.is_reflection = input_reflection
       self.is_result_reflection=True
       self.XOR = final_xor
    def crc8_lookup_table(self):
        generator=self.generator
        for i in range(0,256):
            hash=self.compute_crc8_one_byte(i)
            self.crc8_lookup_table[i]=hash
    def crc8_multibyte_effeciently(self,data:'bytearray'):
        length=len(data)
        crc=self.initial_crc
        for i in range(0,length):
            byte=(input_reflection(data[i],8) if self.is_reflection else data[i])
            crc=self.crc8_lookup_table[(byte^crc)&0xff]^crc
        crc = (input_reflection(crc, 8) if self.is_result_reflection else crc)
        return crc^self.XOR
    def crc8_multibyte(self,data:'bytearray')->'int':
        crc=self.initial_crc
        length=len(data)
        for i in range(0,length):
            byte = (input_reflection(data[i], 8) if self.is_reflection else data[i])
            crc=self.crc8_single(byte,crc)
        crc = (input_reflection(crc, 8) if self.is_result_reflection else crc)
        return crc^self.XOR
    def crc8_single(self,byte,crc=0)->'int':
        crc^=byte
        for i in range(0,8):
            if (crc &0x80)!=0:
                crc=((crc<<1)^self.generator)
            else:
                crc<<=1
        return crc&0x00ff
class Crc16Algo:
    def __init__(self,generator,initial_crc,input_reflection:'bool',result_reflection:'bool',final_xor:'int'):
        self.crc16_lookup_table=[0]*256
        self.generator=generator
        self.initial_crc=initial_crc
        self.is_reflection=input_reflection
        self.is_result_reflection = result_reflection
        self.XOR=final_xor
    def crc16_single(self,byte,crc=0)->'int':
        crc^=(byte<<8)
        length=8
        for i in range(0,length):
            if (crc & 0x8000) !=0:
                crc =((crc <<1) ^ self.generator)
            else:
                crc<<=1
        return (crc&0xffff)
    def crc16_lookuptable_prepare(self)->'None':
        for  u in range(0,256):
            crc=0
            crc^=(u<<8)
            for i in range(0,8):
                if(crc &0x8000 !=0):
                    crc=((crc<<1)^self.generator)
                else:
                    crc<<=1
            self.crc16_lookup_table[u]=(crc&0xffff)
    def crc16_multibyte(self,data:'bytearray')->'int':
        length=len(data)
        crc=self.initial_crc
        for i in range(0,length):
            #step1+2:xor the new crc with the byte left shifted:
            byte = (input_reflection(data[i], 8) if self.is_reflection else data[i])
            crc=self.crc16_single(byte,crc)
        crc = crc & 0xffff
        crc = (input_reflection(crc, 16) if self.is_result_reflection else crc)
        return crc^self.XOR
    def crc16_multibyte_effecient(self,data:'bytearray')->'int':
        length=len(data)
        crc=self.initial_crc
        for i in range(0,length):
            byte = (input_reflection(data[i], 8) if self.is_reflection else data[i])
            index=((crc>>8)^byte)&0xff
            intermediate=self.crc16_lookup_table[index]
            crc=(intermediate)^(crc<<8)
        crc = crc & 0xffff
        crc = (input_reflection(crc, 16) if self.is_result_reflection else crc)
        return crc^self.XOR
class Crc32Algo:
    def __init__(self,generator,initial_crc,input_reflection:'bool',result_reflection:'bool',final_xor):
        self.generator=generator
        self.crc32_lookup_table=[0]*256
        self.initial_crc=initial_crc
        self.is_reflection = input_reflection
        self.is_result_reflection=result_reflection
        self.XOR = final_xor
    def crc32_single(self,byte,crc=0)->'int':
        crc^=(byte <<24)
        for i in range(0,8):
            if ((crc &0x80000000)!=0):
                crc=((crc<<1)^self.generator)
            else:
                crc<<=1
        return crc&0xffffffff
    def crc32_multibyte_effecient(self,data:'bytearray')->'int':
        crc=self.initial_crc
        for i in range(0,len(data)):
            byte = (input_reflection(data[i], 8) if self.is_reflection else data[i])
            index=((byte^(crc>>24)))&0xff
            intermediate=self.crc32_lookup_table[index]
            crc=((crc <<8)^(intermediate))
        crc = crc & 0xffffffff
        crc = (input_reflection(crc, 32) if self.is_result_reflection else crc)
        return crc^self.XOR
    def crc32_multibyte(self,data:'bytearray')->'int':
        crc=self.initial_crc
        for i in range(0,len(data)):
            byte = (input_reflection(data[i], 8) if self.is_reflection else data[i])
            crc=self.crc32_single(byte,crc)
        crc = crc & 0xffffffff
        crc = (input_reflection(crc, 32) if self.is_result_reflection else crc)
        return crc^self.XOR
    def crc32_lookuptable_prepare(self):
        for i in range(0,256):
            crc=((i<<24)&0xffffffff)
            for u in range(0,8):
                if ((crc & 0x80000000)!=0):
                    crc=((crc<<1)^self.generator)
                else:
                    crc<<=1
            self.crc32_lookup_table[i]=(crc&0xffffffff)

hasho=Crc32Algo(0x04C11DB7,0,True,True,0xffffffff)
hasho.crc32_lookuptable_prepare()

tests = [
    b"\x00",
    b"\x80",
    b"A",
    b"ABC",
    b"123456789",
    b"\xDE\xAD\xBE\xEF",
]

for t in tests:
    a = hasho.crc32_multibyte(t)
    b = hasho.crc32_multibyte_effecient(t)
    if(a==b):
        print(hex(a))

#final xor is usually:0xffffffff