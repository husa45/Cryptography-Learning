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
def findCoeffecientEuclidian(x:int,y:int) ->'tuple':
    gcd=GCD(x,y)
    if gcd>1:
        return (1,-1)
    else:
        return extended_euclidian(x,y)
result=findCoeffecientEuclidian(26513,32321)
if(result[0]*26513+result[1]*32321)==1:
    print(min(result))