import sys
import cv2
import numpy as np
from datetime import datetime
import mrcfile
start=datetime.now()
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


# read particle data(only micrograph)
data=relion_data.getRdata()[1]
M= relion_data.getRdata()[0].index( '_rlnMicrographName' )
H= relion_data.getRdata()[0].index( '_rlnHelicalTubeID' )
C= relion_data.getRdata()[0].index( '_rlnClassNumber' )
X= relion_data.getRdata()[0].index( '_rlnCoordinateX' )
Y= relion_data.getRdata()[0].index( '_rlnCoordinateY' )
x= relion_data.getRdata()[0].index( '_rlnOriginX' )
y= relion_data.getRdata()[0].index( '_rlnOriginY' )
print('finish reading')
# extract helical parameters
helicaldic={}
helicalnum=[]
count=-1
for particle in data:
    ID = particle[M]
    dx = float(particle[X])+float(particle[x])
    dy = float(particle[Y])+float(particle[y])
    if ID in helicalnum:
        n=str(count)
        lst=helicaldic[n]
        lst.append([particle[C],float(particle[X]),float(particle[Y])])
        helicaldic[n]=lst
    else:
        helicalnum.append(ID)
        n=str(helicalnum.index(ID))
        count+=1
        helicaldic[n]=[[particle[C],float(particle[X]),float(particle[Y])]]
print('finish converting')
print (datetime.now()-start)

print(helicalnum[0])

for i in range(len(helicalnum)):
    with mrcfile.open(helicalnum[i],permissive=True, mode='r+') as mrc:
        M=mrc.data
    temp_lst=helicaldic[str(i)]
    for j in temp_lst:
        cv2.putText(M, j[0] , (int(round(j[1])),int(round(j[2]))), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 0 , 1, cv2.LINE_AA)
    print(M)
    with mrcfile.new('{}_ori.mrc'.format(helicalnum[i][:-4]),overwrite=True) as mrc1:
        mrc1.set_data(np.zeros((3710, 3838), dtype=np.int8))
        mrc1.data[:][:]=M

print (datetime.now()-start) 
