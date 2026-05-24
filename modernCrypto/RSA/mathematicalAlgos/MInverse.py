from GCD import GCD
def Minverse(pair:list[int])->'int':
    if GCD(pair[0],pair[1])!=1:
        raise SystemExit("The numbers provided must be coprime")
    #arrange in max,min fashion:
    c = pair[0];pair[0] = max(pair[0], pair[1]);pair[1] = min(c, pair[1])
    #find the  cofactors:
    result=0
    I=[[0,1],[1,0]]
    original=pair.copy()
    while True:
        result,remainder = divmod(pair[0], pair[1])
        previous=pair[1]
        pair[1]=(pair[0]-result*pair[1])
        pair[0]=previous
        
        ####################################
        #finding the I:
        sebo1=I[0][0]-result*I[0][1]
        sebo2=I[1][0]-result*I[1][1]
        I[0][0]=I[0][1]
        I[1][0]=I[1][1]
        I[0][1]=sebo1
        I[1][1]=sebo2
        if pair[1]==0:
            break
        ####################################
    coeffecients= (I[0][0],I[1][0])
    return coeffecients[0]
def check(a, n, expected):
    try:
        r = Minverse([a, n])
        ok = (r == expected)
        print(f"[{'OK' if ok else 'FAIL'}] inv({a} mod {n}) = {r}, expected {expected}")
    except Exception as e:
        print(f"[EXCEPTION] inv({a} mod {n}): {e}")
def main():
    print(Minverse([5,6]))
    print("=== BASIC VALID INVERSES ===")
    check(3, 5, 2)
    check(5, 6, 5)
    check(11, 60, 11)
    check(7, 26, 15)
    check(17, 3120, 2753)
    print("\n=== NORMALIZATION TESTS ===")
    check(7, 40, 23)     # raw EE gives -17
    check(9, 26, 3)
    check(17, 43, 38)
if __name__=="__main__":
    main()