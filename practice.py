import cv2
import numpy as np
from datetime import datetime
import mrcfile

start=datetime.now()
with mrcfile.open('./10019/a.mrc',permissive=True, mode='r+') as mrc:
    M=mrc.data
print(np.shape(M))
M[0:100,0:100]=0
print(M)
cv2.putText(M,"Hello World", (100,300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 0 , 1, cv2.LINE_AA)
with mrcfile.new('tmp.mrc',overwrite=True) as mrc1:
    mrc1.set_data(np.zeros((3710, 3838), dtype=np.int8))
    mrc1.data[:][:]=M

print (datetime.now()-start)