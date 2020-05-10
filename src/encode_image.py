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
    image = None
    height = 0
    width = 0
    print("> checking if the file " + fileName + " is in /images directory.")
    if path.exists("./images/" + fileName) == False:
        print("> file " + fileName + " doesn't exist in /image.")
        return None
    else:
        print("> image " + fileName + " found.")
        image = imread("./images/" + fileName,IMREAD_GRAYSCALE)
        print("> image grayscaled.")
        height, width = image.shape[0],image.shape[1]
        print("> image size: " + str(height) + "x" + str(width) + ".")

    # resize if the image cannot be divided by 8x8 block
    if ((height%bl_size != 0) or (width%bl_size != 0)):
        height -= height%bl_size
        width -= width%bl_size
        image = resize(image,dsize=(width,height))
    print("> image resized to " + str(height) + "x" + str(width) + ".")
    num_blocks_h = math.ceil(height/bl_size)
    num_blocks_w = math.ceil(width/bl_size)
    #print(num_blocks_h,num_blocks_w)
    padded_img = np.zeros([height,width])
    padded_img[0:height,0:width] = image[0:height,0:width]
    print("> writing uncompressed bitmap.")
    imwrite("./results/uncompressed.bmp",np.uint8(padded_img))
    
if __name__ == '__main__':
    main()
