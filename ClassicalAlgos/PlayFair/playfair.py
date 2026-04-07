class Algorithm:
    def __init__(self,key:'str',upperCase:'bool'):
        seen=set({})
        self.matrix=[]
        self.upperCase=upperCase
        self.spaces=set({})
        #construct charset:
        charset=key
        seen=set(key)
        rango=None
        if upperCase:
            rango=range(65,91)
        else:
            rango = range(97, 123)

        for i in rango:
            if chr(i) not in seen:
                charset+=chr(i)
        #filling the matrix:
        counter = 0
        row=[]
        for char in charset:
            if char=="I":
                row.append("I/J")
                counter+=1
                continue
            if char=="i":
                row.append("I/J")
                counter += 1
                continue
            if char=="J":
                continue
            row.append(char)
            counter+=1
            if  counter==5:
                self.matrix.append(row)
                row=[]
                counter=0
        print(self.matrix)
    def findChar(self,char:'str')->'tuple':
        """
        param char:Current char to search for
        return:tuple --->(row,column)
        """
        for i in range(0,len(self.matrix)):
            for u in range(0,len(self.matrix[i])):
                if self.matrix[i][u]==char :
                    return (i,u)

    def encrypt(self,plain:'str')->'str':
        """
        param plain: plain text
        return: cipher text using the previosuly passed key
        """
        if plain.index("I")!=-1:
            self.matrix[2][3]="I"
        elif plain.index("J")!=-1:
            self.matrix[2][3] = "I"
        template=""
        encrypted=""
        #preparing the template:

        for i in range(0,len(plain)):
            if i!=len(plain)-1 and (plain[i] ==plain[i+1]):
                template+=plain[i]+('X' if self.upperCase else 'x')
                continue
            elif plain[i]==' ':
                self.spaces.add(i)
                continue
            template+=plain[i]
        if len(template)%2!=0:
            template+=('X' if self.upperCase else 'x')
        print(template)
        for i in range(0,len(template),2):
            charOne=self.findChar(template[i])
            charTwo = self.findChar(template[i+1])
            #same row:
            if charOne[0] ==charTwo[0]:
                encrypted+=self.matrix[charOne[0]][(charOne[1]+1)%5]
                encrypted += self.matrix[charTwo[0]][(charTwo[1] + 1) % 5]
            #same column:
            elif charOne[1]==charTwo[1]:
                encrypted += self.matrix[(charOne[0]+1)%5][charOne[1] ]
                encrypted += self.matrix[(charTwo[0]+1)%5][charTwo[1]]
            #different Rows and columns:
            else:
                encrypted+=self.matrix[charOne[0]][charTwo[1]]
                encrypted += self.matrix[charTwo[0]][charOne[1]]
        return encrypted
    def decrypt(self,encrypted:'str')->'str':
        """
        param encrypted: plain text
        return: plain text using the previosuly passed key
        """
        template=encrypted
        plain=""
        #preparing the template:

        # for i in range(0,len(encrypted)):
        #     if i!=len(encrypted)-1 and (encrypted[i] ==encrypted[i+1]):
        #         template+=encrypted[i]+('X' if self.upperCase else 'x')
        #         continue
        #     template+=encrypted[i]
        # if len(template)%2!=0:
        #     template+=('X' if self.upperCase else 'x')
        print(template)
        for i in range(0,len(template),2):
            charOne=self.findChar(template[i])
            charTwo = self.findChar(template[i+1])
            #same row:
            if charOne[0] ==charTwo[0]:
                plain+=self.matrix[charOne[0]][(charOne[1]-1)%5]
                plain += self.matrix[charTwo[0]][(charTwo[1] - 1) % 5]
            #same column:
            elif charOne[1]==charTwo[1]:
                plain += self.matrix[(charOne[0]-1)%5][charOne[1] ]
                plain += self.matrix[(charTwo[0]-1)%5][charTwo[1]]
            #different Rows and columns:
            else:
                plain+=self.matrix[charOne[0]][charTwo[1]]
                plain += self.matrix[charTwo[0]][charOne[1]]
        #clean repeated chars:
        cleanedPlain=""
        u=0
        i=0
        while True:
            if u in self.spaces:
                cleanedPlain+=' '
                u+=1
                continue
            if i==len(plain)-1:
                break
            if plain[i]=='X' and i!=len(plain)-1 and i!=0:
                if plain[i-1]==plain[i+1]:
                    i+=1
                    u+=1
                    continue
            cleanedPlain+=plain[i]
            i+=1
            u+=1
        if cleanedPlain[-1]=='X' and len(cleanedPlain)-1 %2!=0:
            cleanedPlain=cleanedPlain[:-1]
        return cleanedPlain
algo=Algorithm("MONARCHY",True)
result=algo.encrypt("I LOVE RE SO MUCH BUT AI IS TAKING OVER")
print(algo.decrypt(result))
