import png
import image
import os
from vec import Vec
from mat import Mat

X_VALUE = 166
Y_VALUE = 189

def file2image(path):
     (w, h, p, m) = png.Reader(filename = path).asRGBA()
     return [image._flat2boxed(r) for r in p]

def image2file(image, path):
     """ Writes an image in list of lists format to a file. Will work with either color or grayscale. """
     if image.isgray(image):
         img = image.gray2color(image)
     else:
         img = image
     with open(path, 'wb') as f:
         png.Writer(width=len(image[0]), height=len(image)).write(f, [_boxed2flat(r) for r in img])
 
def color2gray(image):
     """ Converts a color image to grayscale """
     # we use HDTV grayscale conversion as per https://en.wikipedia.org/wiki/Grayscale
     return [[int(0.2126*p[0] + 0.7152*p[1] + 0.0722*p[2]) for p in row] for row in image]
 
def load_images(directoryname, num_faces = 2):
     return {i:color2gray(file2image(os.path.join(directoryname,"img%02d.png" % i))) for i in range(num_faces)}
     #loads the given number of image files from the classified files
     #returns a dict of face number to image files
 
def find_centroid(veclist):
     num_vecs = len(veclist)
     vec = {}
     for r in veclist[0].D:
         avg = 0
         for p in range(num_vecs):
             avg += veclist[p][r]
         avg = avg/num_vecs
         vec[r] = avg
     return Vec(veclist[0].D, vec)
 
def vec2listlist(vec):
    listlist = []
    for p in range(Y_VALUE):
        tmp_list = []
        for i in range(X_VALUE):
            tmp_list += [vec[(i,p)]]
        listlist += tmp_list
    return listlist


image_dict = load_images("faces")
D = {(x,y) for x in range(X_VALUE) for y in range(Y_VALUE)}
face_images = {r:Vec(D,{(x,y):image_dict[r][y][x] for y in range(len(image_dict[r])) for x in range(len(image_dict[r][y]))}) for r in image_dict}

centroid = find_centroid([face_images[r] for r in face_images])
print(centroid)

image.image2file(centroid, "")
'''
image.image2display(vec2listlist(centroid), None)
'''
