def GCD(x:int,y:int)->'int':
    c=x;x=max(x,y);y=min(c,y)
    result,remainder=divmod(x,y)
    x=y;y=remainder
    if y==0:
        return x
    while y!=0:
        result,remainder=divmod(x,y)
        x=y
        y=remainder
    else:
        return x
def extended_euclidian(x:int,y:int)->'tuple':
    #finding the maximum:
    copy=x;x=max(x,y);y=min(copy,y)
    
    previous=(y,1,0)
    quotient=x//y
    next=(x-y*quotient,0-1*quotient,1)
    while next[0]!=1:
        copy=next
        quotient=previous[0]//next[0]
        next=(previous[0]-next[0]*quotient,previous[1]-next[1]*quotient,previous[2]-next[2]*quotient)
        previous=copy
    return next[1::]


def FindCoeffeientsEuclidian(pair: list[int]) -> 'int':
    if GCD(pair[0], pair[1]) != 1:
        # raise SystemExit("The numbers provided must be coprime")
        return 0
    # arrange in max,min fashion:
    original = pair.copy()
    c = pair[0];
    pair[0] = max(pair[0], pair[1]);
    pair[1] = min(c, pair[1])
    # find the  cofactors:
    result = 0
    I = [[0, 1], [1, 0]]

    while True:
        result, remainder = divmod(pair[0], pair[1])
        previous = pair[1]
        pair[1] = (pair[0] - result * pair[1])
        pair[0] = previous

        ####################################
        # finding the I:
        sebo1 = I[0][0] - result * I[0][1]
        sebo2 = I[1][0] - result * I[1][1]
        I[0][0] = I[0][1]
        I[1][0] = I[1][1]
        I[0][1] = sebo1
        I[1][1] = sebo2
        if pair[1] == 0:
            break
        ####################################
    coeffecients = (I[0][0], I[1][0])
    return coeffecients

