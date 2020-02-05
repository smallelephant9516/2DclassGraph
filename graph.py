import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import networkx as nx
from datetime import datetime

#start
start=datetime.now()
print (datetime.now()-start)


#import .star file
class read_relion(object):

    def __init__(self, file):
        self.file = file
        
        
    def getRdata(self):
        Rvar = [] #read the variables 
        Rdata = [] # read the data

        for star_line in open(self.file).readlines():
            if star_line.find("_rln") != -1:
                var = star_line.split()
                Rvar.append(var[0])
            #    Rvar_len = Rvar_len+1
            elif star_line.find("data_") != -1 or star_line.find("loop_") != -1 or len(star_line.strip()) == 0:
                continue
                
            else:
                Rdata.append(star_line.split())
                
        return Rvar, Rdata

def column(matrix, i):
    return [row[i] for row in matrix]

# combination of 0 and 1
def combination(n):
    loop=[]
    for i in range(1<<n):
        s=bin(i)[2:]
        s='0'*(n-len(s))+s
        loop.append(list(s))
    return loop

def permutation(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return 'r is more than n'
    indices = list(range(n))
    cycles = list(range(n, n-r, -1))
    yield list(pool[i] for i in indices[:r])
    while True:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield list(pool[i] for i in indices[:r])
                break
        else:
            return

def factorial(n):
    a=1
    i=0
    while i<=n:
        i+=1
        a*=i
    return a

def get_index(lst,item):
    return [i for i in range(len(lst)) if lst[i] == item]

def find_array(arr,lst):
    for i, j in enumerate(arr):
        if list(j)==lst:
            return True
    return False


relion_data = read_relion(sys.argv[1])
#average_data=read_relion(sys.argv[2])


# create empty class matrix
classgroup=[]
for i in range(50):
    classgroup.append(str(i+1))
#average=average_data.getRdata()[1]
#for i in average:
#    classgroup.append(i[-1])
matrix = np.zeros([len(classgroup),len(classgroup)],dtype=int)
print(classgroup)


# read particle data
data=relion_data.getRdata()[1]
M= relion_data.getRdata()[0].index( '_rlnImageName' )
H= relion_data.getRdata()[0].index( '_rlnHelicalTubeID' )
C= relion_data.getRdata()[0].index( '_rlnClassNumber' )
print('finish reading')
# extract helical parameters
helicaldic={}
helicalnum=[]
count=-1
for particle in data:
    ID = particle[M][7:]+'-'+str(particle[H])
    if ID in helicalnum:
        n=str(count)
        lst=helicaldic[n]
        lst.append(particle[C])
        helicaldic[n]=lst
    else:
        helicalnum.append(ID)
        n=str(helicalnum.index(ID))
        count+=1
        helicaldic[n]=[particle[C]]
print('finish converting')


# produce weight matrix
for n in range(len(helicalnum)):
    helix=helicaldic[str(n)]
    for i in range(len(helix)-1):
        a=classgroup.index(helix[i])
        b=classgroup.index(helix[i+1])
        matrix[a][b]=matrix[a][b]+1

M=matrix


#delete empty column
delgroup=[]
for i in range(len(classgroup)):
    n=1
    for j in matrix[i]:
        if j!=0:
            print('out')
            break
        else:
            if n<len(classgroup):
                n=n+1
                continue
            else:
                print('del')
                delgroup.append(i)
                break

delgroup.sort()
print(delgroup)
n=0
for i in delgroup:
    M = np.delete(M,i-n,0)
    M = np.delete(M,i-n,1)
    n=n+1
    classgroup.remove(str(i+1))

print(M)
print(classgroup)
#n=0
#for i in range(1,4):
#    M = np.delete(M,i-n,0)
#    M = np.delete(M,i-n,1)
#    n=n+1
#classgroup.remove('2')
#classgroup.remove('7')
#classgroup.remove('11')
NS=M


# produce symmetric matrix
S=np.tril(NS)+np.tril(NS.T, -1)
print(S)

# select M or S
Mclean=S


#produce weight matrix
MW = np.zeros([len(classgroup),len(classgroup)],dtype=float)
for i in range(len(classgroup)):
    sum = np.sum(Mclean[i])
    for j in range(len(Mclean[i])):
        MW[i][j]=Mclean[i][j]/sum

print(MW)


# produce adjacency matrix
MA = np.zeros([len(classgroup),len(classgroup)],dtype=int)
for i in range(len(classgroup)):
    lst=Mclean[i]
    l=len(lst)
    keep=np.argsort(lst)
    lst=np.zeros((l),dtype=int)
    for j in range(len(classgroup)):
        lst[keep[-(j+1)]]=1
    MA[i]=lst

# delete the self cycle
for i in range(len(classgroup)):
    MA[i][i]=0


print(MA)
print (datetime.now()-start)

# find all the cycles

comb=combination(len(classgroup))
print('combination')
pweight=[]
all_cycles=[]
all_weights=[]
names=[]
for i in range(len(comb)):
    lst=comb[i]
    node=get_index(lst, str(1))
    n=lst.count(str(1))
    if n<4:
        continue
    root=min(node)      # find start node
    all_node=node
    node.remove(root)
    print(all_node)
    print (datetime.now()-start)
    weight=[]
    loop=[]
    for value in permutation(node,len(node)):        # permutation for the rest node to find all the cycles
        value_reverse=value[::-1]
        value_reverse.append(root)
        if find_array(loop,value_reverse) is True:
            continue
        else:
            value.append(root)
            loop.append(value)
    print('all the loops are detected for {} nodes'.format(all_node))
    
    #make name for each combination of nodes
    name=''
    for i in range(len(all_node)):
        name=name+','+str(classgroup[all_node[i]])
    names.append(name)
    for i in range(len(loop)):
        wi=0
        tem=loop[i]
        print(tem)
        for j in range(len(tem)):
            j_0=tem[1]
            j_n=tem[j]
            if j <=len(tem)-2:
                j_n1=tem[j+1]
                wi+=MW[j_n][j_n1]+MW[j_n1][j_n]
            else:
                wi+=MW[j_n][j_0]+MW[j_0][j_n]
        relative_wi=wi/n
        weight.append(relative_wi)
    
    all_cycles.append(loop)
    all_weights.append(weight)
        

print (datetime.now()-start)
ks=[]
ls=[]
for i in all_weights:
    k=max(i)
    ks.append(k)
    l=i.index(max(i))
    ls.append(l)
h=max(ks)
hi=ks.index(h)
print(h,names[hi])
#Statements

print (datetime.now()-start)

# produce graph from adjacency marix
G= nx.Graph()
G.add_nodes_from(classgroup)
for i in range(len(classgroup)):
    for j in range(len(classgroup)):
        if (MA[i][j]!=0):
            G.add_edge(classgroup[i],classgroup[j], weight=MW[i][j])
        else:
            continue
# draw image

nx.draw_networkx(G, with_labels=True, arrows=True, font_weight='bold')
plt.show()