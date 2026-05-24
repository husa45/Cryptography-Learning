from GCD import extended_euclidian


def CRT(matrix:list[int])->'int':
    #finding Multiplicative inverse
    M=1
    MX=[]
    for row in matrix:
       M*=int(row[1])
    for row in matrix:
        MX.append(M/int(row[1]))
    MInverses=[]
    i=0
    for row in matrix:
        MInverses.append(extended_euclidian(MX[i],int(row[1]))[1] %int(row[1]))
        i+=1
    result=0
    i=0
    while i<len(MX):
        result+=(int(matrix[i][0])*MX[i]*MInverses[i])
        i+=1
    return result %M
def main():
    matrix:list[int]=[]
    print("enter the equations constants (An then Mn ) ,seperated by space")
    while (provided:=input()):
        matrix.append(provided.split())
    print(CRT(matrix))





if __name__=="__main__":
    main()