# src/dct.py

import numpy as np
from math import cos, pi, sqrt

def dct_2d(image):
    image = np.asarray(image)
    height,width = image.shape
    imageRow = np.zeros_like(image).astype(float)
    imageCol = np.zeros_like(image).astype(float)

    for h in range(height):
        image[h,:] = dct_1d(image[h,:])
    for w in range(width):
        image[:, w] = dct_1d(image[:, w])
    #return imageCol

def dct_1d(image):
    n = len(image)
    newImage= np.zeros_like(image).astype(float)

    for k in range(n):
        sum = 0
        for i in range(n):
            sum += image[i] *\
                cos(2*pi*k/(2.0*n)*i+(k*pi)/(2.0*n))
        ck = sqrt(0.5) if k == 0 else 1
        newImage[k] = sqrt(2.0 / n) * ck * sum
    
    # Comment this out later
    for i in range(n):
        if ((newImage[i] > -1) and (newImage[i] < 1)):
            newImage[i] = 0
    return newImage
