# version code 45c3e5429d04
# Please fill out this stencil and submit using the provided submission script.

from vec import Vec
from mat import Mat, transpose
from vecutil import list2vec
from matutil import mat2rowdict, rowdict2mat, mat2coldict
from math import sqrt

import svd
import matutil

import eigenfaces



def find_centroid(veclist):
    '''
    Input:
        - veclist: a list of Vecs
    Output:
        - a Vec, the centroid of veclist
    Example:
        >>> from vecutil import list2vec
        >>> vs = [list2vec(l) for l in [[1,2,3],[2,3,4],[9,10,11]]]
        >>> find_centroid(vs)
        Vec({0, 1, 2},{0: 4.0, 1: 5.0, 2: 6.0})
    '''
    num_vecs = len(veclist)
    vec = {}
    for r in veclist[0].D:
        avg = 0
        for p in range(num_vecs):
            avg += veclist[p][r]
        avg = avg/num_vecs
        vec[r] = avg
    return Vec(veclist[0].D, vec)

## Task 1

# see documentation of eigenfaces.load_images
image_dict = eigenfaces.load_images("faces")
D = {(x,y) for x in range(166) for y in range(189)}
face_images = {r:Vec(D,{(x,y):image_dict[r][y][x] for y in range(len(image_dict[r])) for x in range(len(image_dict[r][y]))}) for r in image_dict} # dict of Vecs

## Task 2

centroid = find_centroid([face_images[r] for r in face_images])
centered_face_images = {r:face_images[r]- centroid for r in face_images}

## Task 3

A = rowdict2mat(centered_face_images) # centered image vectors
V, Sigma, U = svd.factor(transpose(A))
VT = mat2coldict(V)
orthonormal_basis = rowdict2mat([VT[r] for r in range(10)]) # 10 rows

## Task 4

#This is the "transpose" of what was specified in the text.
#Follow the spec given here.
def projected_representation(M, x):
    '''
    Input:
        - M: a matrix with orthonormal rows with M.D[1] == x.D
        - x: a vector
    Output:
        - the projection of x onto the row-space of M
    Examples:
        >>> from vecutil import list2vec
        >>> from matutil import listlist2mat
        >>> x = list2vec([1, 2, 3])
        >>> M = listlist2mat([[1, 0, 0], [0, 1, 0]])
        >>> projected_representation(M, x)
        Vec({0, 1},{0: 1, 1: 2})
        >>> M = listlist2mat([[3/5, 1/5, 1/5], [0, 2/3, 1/3]])
        >>> projected_representation(M, x)
        Vec({0, 1},{0: 1.6, 1: 2.333333333333333})
    '''
    return M*x

## Task 5

#This is the "transpose" of what was specified in the text.
#Follow the spec given here.
def projection_length_squared(M, x):
    '''
    Input:
        - M: matrix with orthonormal rows with M.D[1] == x.D
        - x: vector
    Output:
        - the square of the norm of the projection of x into the
          row-space of M
    Example:
        >>> from vecutil import list2vec
        >>> from matutil import listlist2mat
        >>> x = list2vec([1, 2, 3])
        >>> M = listlist2mat([[1, 0, 0], [0, 1, 0]])
        >>> projection_length_squared(M, x)
        5
        >>> M = listlist2mat([[3/5, 1/5, 1/5], [0, 2/3, 1/3]])
        >>> projection_length_squared(M, x)
        5.644424691358024
    '''

    A = projected_representation(M,x)
    B = A*M
    norm = 0
    for a in B.D:
        norm += B[a]**2
    return norm



## Task 6

#This is the "transpose" of what was specified in the text.
#Follow the spec given here.
def distance_squared(M, x):
    '''
    Input:
        - M: matrix with orthonormal rows with M.D[1] == x.D
        - x: vector
    Output:
        - the square of the distance from x to the row-space of M
    Example:
        >>> from vecutil import list2vec
        >>> from matutil import listlist2mat
        >>> x = list2vec([1, 2, 3])
        >>> M = listlist2mat([[1, 0, 0], [0, 1, 0]])
        >>> distance_squared(M, x)
        9
        >>> M = listlist2mat([[3/5, 1/5, 1/5], [0, 2/3, 1/3]])
        >>> distance_squared(M, x)
        8.355575308641976
    '''
    A = projection_length_squared(M,x)
    return (x*x-A)
    

## Task 7

X = mat2rowdict(A)
distances_to_subspace = [distance_squared(orthonormal_basis, X[x]) for x in X]


## Task 8

unclass_dict = eigenfaces.load_images("unclassified", 10)
unclass_images = {r:Vec(D,{(x,y):unclass_dict[r][y][x] for y in range(len(unclass_dict[r])) for x in range(len(unclass_dict[r][y]))}) for r in unclass_dict}
centered_unclass_images = {r:unclass_images[r]- centroid for r in unclass_images}

distances = [distance_squared(orthonormal_basis, centered_unclass_images[x]) for x in centered_unclass_images]
'''
print(distances)
'''
classified_as_faces = set([1,2,3,4,5]) # of dictionary keys

## Task 9


threshold_value = (sum(distances_to_subspace)/20) *6

## Task 10

#This is the "transpose" of what was specified in the text.
#Follow the spec given here.
def project(M, x):
    '''
    Input:
        - M: an orthogonal matrix with row-space equal to x's domain
        - x: a Vec
    Output:
        - the projection of x into the column-space of M
    Example:
        >>> from vecutil import list2vec
        >>> from matutil import listlist2mat
        >>> x = list2vec([1, 2, 3])
        >>> M = listlist2mat([[1, 0], [0, 1], [0, 0]])
        >>> project(M, x)
        Vec({0, 1, 2},{0: 1, 1: 2, 2: 0})
        >>> M = listlist2mat([[3/5, 0], [1/5, 2/3], [1/5, 1/3]])
        >>> project(M, x)
        Vec({0, 1, 2},{0: 0.96, 1: 1.8755555555555554, 2: 1.0977777777777777})
    '''
    A = projected_representation(M,x)
    return A*M
    

## Task 11

# see documentation for image.image2display

## Task 12

