def func1(a,b,c,d):
    a+=1
    b+=1
    c+=1
    d+=1

    a+=b
    c+=d
    b+=a
    d+=c

    a*=b
    c*=d
    b*=a
    d*=c

    a-=b
    c-=d
    b-=a
    d-=c
    return a+b+c+d


def func2(r):
    return 3.14*2*r
    
    
def func3(r):
    return 3.14*(r+r)


