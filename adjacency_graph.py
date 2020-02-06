import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import networkx as nx



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
    for j in range(2):
        lst[keep[-(j+1)]]=1
    MA[i]=lst

print(MA)


# produce graph from adjacency marix
G= nx.Graph()
G.add_nodes_from(classgroup)
for i in range(len(classgroup)):
    for j in range(len(classgroup)):
        if (MA[i][j]!=0) & (MW[i][j]>=0.1):
            G.add_edge(classgroup[i],classgroup[j], weight=MW[i][j])
        else:
            continue

nx.draw_networkx(G, with_labels=True, arrows=True, font_weight='bold')
plt.show()