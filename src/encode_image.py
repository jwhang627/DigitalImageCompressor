# src/encode_image.py

import numpy as np
import math
from cv2 import *
from sys import *
from zigzag import *
from huffman import *
from os import *

bl_size = 8

# Quantization Matrix
QUANTIZATION_MAT = np.array([[16,11,10,16, 24, 40, 51, 61],\
                             [12,12,14,19, 26, 58, 60, 55],\
                             [14,13,16,24, 40, 57, 69, 56],\
                             [14,17,22,29, 51, 87, 80, 62],\
                             [18,22,37,56, 68,109,103, 77],\
                             [24,35,55,64, 81,104,113, 92],\
                             [49,64,78,87,103,121,120,101],\
                             [72,92,95,98,112,100,103, 99]])

def get_bitstream(img):
    bits = ""
    skip = 0
    stream = []
    for i in range(img.shape[0]):
        if img[i] != 0:
            stream.append((img[i],skip))
            bits += str(img[i]) + " " + str(skip) + " "
        else:
            skip += 1
    return bits

def main():
    fileName = argv[1]
    image = 0
    print("> checking if the file " + fileName + " is in /image directory.")
    if exists("/images" + fileName) == false:
        print("> file " + fileName + " doesn't exist in /image.")
    else:
        print("> image " + fileName + " found.")
        image = imread(fileName)
    print(image[0:1])
