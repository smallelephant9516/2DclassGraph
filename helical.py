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
for i in range(10):
    print(helicaldic[str(i)])
# output helical
with open("helical.txt","a") as f:
    for i in range(len(helicalnum)):
        lst=helicaldic[str(i)]
        for j in range(len(lst)):
            if j==len(lst)-1:
                f.write(lst[j]+'\n')
            else:
                f.write(lst[j]+' ')