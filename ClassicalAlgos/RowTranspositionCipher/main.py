from re import *
def encrypt(plainText:'str',key:'list')->'str':
    spaces=set({})
    keySize=len(key)
    matrix=[]
    row=[]
    u=0
    for char in plainText:
        if char!=' ':
            row.append(char)
        else:
            spaces.add(u)
        u+=1
    rowLength=len(row)
    while rowLength % keySize!=0:
        row.append("x")
        rowLength=len(row)
    rowCount=rowLength//keySize
    cipherText=""

    for bito in key:
        indexo=int(bito)-1
        current=""
        for k in range(0,rowCount):
            if k==0:
                current+=row[int(bito)-1]
            else:
                indexo = keySize +indexo
                current+=row[indexo if indexo<rowLength else indexo-keySize]
        cipherText+=current
        current=""
    result=""
    i=0
    u=0
    while i<rowLength:
        if i in spaces:
            result+=' '
            i+=1
            rowLength+=1
        else:
            result+=cipherText[u]
            u+=1
            i+=1
    return result
def decrypt(cipherText:'str',key:'list')->'str':
    spaces = set({})
    keySize = len(key)
    rowCount=len(cipherText)//keySize
    meta=""
    u=0
    for char in cipherText:
         if char != ' ':
            meta+=char
         else:
            spaces.add(u)
         u += 1
    columns=[  meta[i:i+rowCount]  for i in range(0,len(meta),rowCount)]
    meta2=[0]*len(meta)
    u=0
    plainText=""
    for bito in key:
        indexo = int(bito) - 1
        current = columns[u]
        for k in range(0, len(current)):
            if k == 0:
                meta2[indexo]=current[k]
            else:
                indexo = keySize + indexo
                meta2[indexo]=current[k]#[indexo if indexo < rowLength else indexo - keySize]
        #cipherText += current
        current = []
        u+=1
    plainText=''.join(meta2)
    result = ""
    i = 0
    u = 0
    rowLength=len(plainText)
    while i < rowLength:
        if i in spaces:
            result += ' '
            i += 1
            rowLength += 1
        else:
            result += plainText[u]
            u += 1
            i += 1
    return result






def main():
    print("#"*70,end="\n\n")
    print("Row transposition Cipher helper",end="\n\n")
    print("#" * 70,end="\n\n")
    choice:'int'=int(input("Enter 1 to encrypt , or 2 to decrypt : "))
    match choice:
        case 1:
            key=input("Enter the key : ")
            key=findall(r"\d",key)
            plainText:'str'=input("Enter the plaintext :  ")
            result=encrypt(plainText,key)
            print("Result  : ",result,sep="\n")
        case 2:
            key = input("Enter the key : ")
            key = findall(r"\d", key)
            cipherText: 'str' =input("Enter the ciphertext :  ")
            result = decrypt(cipherText, key)
            print("Result  : ", result, sep="\n")
        case _:
            raise SystemExit("No such choice ,try again!!!!")

if __name__=="__main__":
    main()