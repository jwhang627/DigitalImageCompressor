# src/decode_image.py

import cv2
import numpy as np
import math
import json
import os

# import zigzag functions
from zigzag import *
from huffman import *

Q_MAT = np.array([[16,11,10,16,24,40,51,61],\
                  [12,12,14,19,26,58,60,55],\
                  [14,13,16,24,40,57,69,56 ],\
                  [14,17,22,29,51,87,80,62],\
                  [18,22,37,56,68,109,103,77],\
                  [24,35,55,64,81,104,113,92],\
                  [49,64,78,87,103,121,120,101],\
                  [72,92,95,98,112,100,103,99]])

# huffman decoding
print("> opening saved huffman code txt file.")
img = None
with open("./results/huffman_encode.txt", 'r') as o_bin:
    img = o_bin.read()
data = json.load(open("./results/hufftree.json"))
o_bin.close()
decode = huffmanDecode(img,data)

d_f = open("./results/decoded_huff.txt","w")
d_f.write(decode)
d_f.close()

print("> huffman code file opened and decoded."\
      +" saving decoded huffman file"\
      +" as \"./results/decoded_huff.txt\"")

# defining block size
block_size = 8

# parsing
print("> parsing data from encoding.")
details = decode.split()
h = int(''.join(filter(str.isdigit, details[0])))
w = int(''.join(filter(str.isdigit, details[1])))
array = np.zeros(h*w).astype(int)

# this loop gives us reconstructed array of size of image
# some loop var initialisations
k = 0
i = 2
x = 0
j = 0

while k < array.shape[0]:
    if(details[i] == ';'): # break
        break
    
    if "-" not in details[i]:
        array[k] = int(''.join(filter(str.isdigit, details[i])))        
    else:
        array[k] = -1*int(''.join(filter(str.isdigit, details[i])))        

    if(i+3 < len(details)):
        j = int(''.join(filter(str.isdigit, details[i+3])))

    if j == 0:
        k = k + 1
    else:                
        k = k + j + 1        

    i = i + 2

array = np.reshape(array,(h,w))

print("> parsing encoded txt file done.")
print("> decoding through inverse quantization,"\
      +" zig-zag scan, and inverse dct.")
# loop for IDCT
i = 0
j = 0
k = 0

# initialisation of compressed image
padded_img = np.zeros((h,w))

while i < h:
    j = 0
    while j < w:        
        temp_stream = array[i:i+block_size,j:j+block_size]                
        block = inverse_zigzag(temp_stream.flatten(), \
                               int(block_size),int(block_size))            
        de_quantized = np.multiply(block,Q_MAT)                
        padded_img[i:i+block_size,j:j+block_size]\
            = cv2.idct(de_quantized)        
        j += block_size        
    i += block_size

print("> three tasks finished.")

# clamping to  8-bit max-min values
padded_img[padded_img > 255] = 255
padded_img[padded_img < 0] = 0

# compressed image is written
cv2.imwrite("./results/compressed_image.bmp",np.uint8(padded_img))
print("> finished decoding."+\
      " it is now saved as \"./results/decoded_compressed_image.bmp\"")

print("> checking PSNR value of compressed and uncompressed images.")
cmd = 'python3 src/psnr.py'
os.system(cmd)
