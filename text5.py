import sys
import os

def func1(a='hello', b='world'):
    return a + b    

def func2(a= [1,2,3,4,5,6]):
    return [i**2 for i in a]

def func3(a =(1,2,3,45), even = [], flag = False):
    for i in a:
        if i % 2 == 0 and flag:
            even.append(i)

    return even     

def func4(a=[1],b=[2], c=[3], bool = False):
    return a + b + c