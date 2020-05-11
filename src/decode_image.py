# src/decode_image.py

import numpy as np
import math
#import pickle
import json
from cv2 import *
from sys import *
from zigzag import *
from huffman import *
from os import path

bl_size = 8

Q_MAT = np.array([[16,11,10,16, 24, 40, 51, 61],\
                  [12,12,14,19, 26, 58, 60, 55],\
                  [14,13,16,24, 40, 57, 69, 56],\
                  [14,17,22,29, 51, 87, 80, 62],\
                  [18,22,37,56, 68,109,103, 77],\
                  [24,35,55,64, 81,104,113, 92],\
                  [49,64,78,87,103,121,120,101],\
                  [72,92,95,98,112,100,103, 99]])

def main():
    img = None
    # decoding
    print("> decoding binary file back.")
    with open("./results/bitstream.bin","r") as open_bin:
        img = open_bin.read()
    data = json.load(open("./results/hufftree.json"))
    open_bin.close()
    decode = huffmanDecode(img,data)
    details = decode.split()
    print("> done decoding.")

    # parsing data
    print("> parsing data")
    h = int(''.join(filter(str.isdigit,details[0])))
    w = int(''.join(filter(str.isdigit,details[1])))

    #details = details.split()
    
    array = np.zeros([h,w]).astype(int)
    
    i = 2
    j = 0
    k = 0
    while details[i] != ';':
        array[j][k] = details[i]
        if k >= w:
            k = 0
            j += 1
        i += 1

    """
    k = 0
    i = 2
    x = 0
    j = 0

    while k < array.shape[0]:
        if (details[i] == ';'): # break
            break
        if "-" not in details[i]:
            array[k] = int(''.join(filter(str.isdigit, details[i])))
        else:
            array[k] = -1*int(''.join(filter(str.isdigit, details[i])))

        if (i + 3 < len(details)):
            j = int(''.join(filter(str.isdigit, details[i+3])))

        if j == 0:
            k += 1
        else:
            k += j + 1
        i += 2

    i = 0
    j = 0
    k = 0
    """
    padded_img = np.zeros([h,w])
    print("> done parsing binary file.")
    print("> decoding through inverse quantization, zig-zag scan, and inverse dct.")
    # decoding through inverse quantization, zig-zag scan, and inverse DCT
    while i < h:
        j = 0
        while j < w:
            temp_stream = array[i:i+bl_size,j:j+bl_size]
            bl = izigzag(temp_stream.flatten(),\
                         int(bl_size), int(bl_size))
            de_q = np.multiply(bl,Q_MAP)
            padded_img[i:i+bl_size,j:j+bl_size] = idct(de_q)
            j += bl_size
        i += bl_size

    padded_img[padded_img > 255] = 255
    padded_img[padded_img < 0] = 0

    imwrite("./results/decoded_compressed_image.bmp",np.uint8(padded_img))
    print("> done decoding. it is saved as \"./results/decoded_compressed_image.bmp\"")

if __name__ == "__main__":
    main()
