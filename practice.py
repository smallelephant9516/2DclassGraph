import numpy as np
from datetime import datetime
start=datetime.now()


def get_index(lst,item):
    return [i for i in range(len(lst)) if lst[i] == item]
def combination(n):
    loop=[]
    for i in range(1<<n):
        s=bin(i)[2:]
        s='0'*(n-len(s))+s
        loop.append(list(s))
    return loop
a=combination(3)
#Statements

print (datetime.now()-start)