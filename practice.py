import cv2
import numpy as np
from datetime import datetime
import mrcfile

start=datetime.now()
with mrcfile.open('./a.mrc',permissive=True, mode='r+') as mrc:
    M=mrc.data

with mrcfile.new('tmp.mrc',overwrite=True) as mrc1:
    mrc1.set_data(np.zeros((3710, 3838), dtype=np.int8))
    mrc1.data[:][:]=M

print (datetime.now()-start)