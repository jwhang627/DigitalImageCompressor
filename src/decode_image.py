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
    print("> decoding binary file back.")
    with open("./results/bitstream.bin","r") as open_bin:
        img = open_bin.read()
    data = json.load(open("./results/hufftree.json"))
    #print(img)
    #print(data)
    open_bin.close()
    decode = huffmanDecode(img,data)
    print(decode)

if __name__ == "__main__":
    main()
