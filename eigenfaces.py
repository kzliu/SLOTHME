from image import color2gray, file2image
import os
   
def load_images(directoryname, num_faces = 20):
	#loads the given number of image files from the classified files
	#returns a dict of face number to image files
    return {i:color2gray(file2image(os.path.join(directoryname,"img%02d.png" % i))) for i in range(num_faces)}

from mat import *
from math import sqrt
M_f = {(0,0):1/sqrt(2) , (1,0):1/sqrt(2) , (0,1):1/sqrt(3), (1,1):-1/sqrt(3), (2,1):1/sqrt(3)}
test_M = Mat(({0,1,2},{0,1}), M_f)
test_x = Vec({0,1,2}, {0:10,1:20,2:30})
