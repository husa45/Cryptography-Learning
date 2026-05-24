#finding the quadratic residue:




def eulers_criterion(x:int,p:int)->'bool':
    return pow(x,(p-1)//2,p)==1
def quadratic_residue(x:int,p:int):
    if not eulers_criterion(x,p):
        raise SystemExit("x Is quadratic non residue!!!\n")
    i=1
    while True:
        if (i**2)%p ==x:
            return (+i,-1*i)
        i+=1
def main():
    pass
if __name__=="__main__":
    main()