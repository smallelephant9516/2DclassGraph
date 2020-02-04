import numpy as np
def get_index(lst,item):
    return [i for i in range(len(lst)) if lst[i] == item]
def combination(n):
    loop=[]
    for i in range(1<<n):
        s=bin(i)[2:]
        s='0'*(n-len(s))+s
        loop.append(list(s))
    return loop
def findByRow(mat, row):
    return np.where((mat == row).all(1))[0]
a=combination(3)
print(findByRow(a, ['0','1','1']))
