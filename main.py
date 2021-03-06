import png
import string
import base64
import image
import cStringIO
import os
import webbrowser
import tempfile
import sqlite3
import datetime
from PIL import Image
from flask import Flask, request, session, g, redirect, url_for, \
abort, render_template, flash
from contextlib import closing

from vec import Vec
from mat import Mat

# creating our application
app = Flask(__name__)
app.config.from_object(__name__)
app.config['DEBUG'] = True

X_VALUE = 640
Y_VALUE = 480

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
 
def transform(veclist, gradient):
     num_vecs = len(veclist)
     vec = {}
     for r in veclist[0].D:
          new_val = ((1-gradient)*veclist[0][r]) + (gradient*veclist[1][r])
          vec[r] = new_val
     return Vec(veclist[0].D, vec)
 
def vec2listlist(vec):
    listlist = []
    for p in range(Y_VALUE):
        tmp_list = []
        for i in range(X_VALUE):
            tmp_list += [vec[(i,p)]]
        listlist.append(tmp_list)
    return listlist

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

@app.route('/', methods=['GET'])
def index():
     return render_template('index.html', title = 'SLOTHME')

@app.route('/grab', methods=['POST'])
def grab_pic():
     print(request)
     # import pdb; pdb.set_trace()
     photo = cStringIO.StringIO(base64.b64decode(request.form['photo']))
     i = Image.open(photo)
     i.save("faces/img00.png", "png")
     # image.image2file(i, "/tmp/faces/received.png")

     response = app.make_response(url_for('static', filename=slothize(string.atof(request.form['gradient']))))

     response.headers.add('Last-Modified', datetime.datetime.now())
     response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
     response.headers.add('Pragma', 'no-cache')

     return response

def slothize(gradient):
     image_dict = load_images("faces")
     D = {(x,y) for x in range(X_VALUE) for y in range(Y_VALUE)}
     face_images = {r:Vec(D,{(x,y):image_dict[r][y][x] for y in range(len(image_dict[r])) for x in range(len(image_dict[r][y]))}) for r in image_dict}
     slothd = transform([face_images[r] for r in face_images], gradient)
     image.image2file(vec2listlist(slothd), "static/slothd.png")


     return "slothd.png"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
