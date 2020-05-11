# src/encode_image.py

import numpy as np
import math
import sys
import json

# import zigzag functions
from zigzag import *
from huffman import *
from sys import *
from os import path
from cv2 import *

def get_bitstream(image):
    i = 0
    skip = 0
    stream = []    
    bitstream = ""
    image = image.astype(int)
    while i < image.shape[0]:
        if image[i] != 0:            
            stream.append((image[i],skip))
            bitstream = bitstream + \
                str(image[i])+ " " +str(skip)+ " "
            skip = 0
        else:
            skip = skip + 1
        i = i + 1
    return bitstream

# defining block size
block_size = 8

# Quantization Matrix 
Q_MAT = np.array([[16,11,10,16,24,40,51,61],\
                  [12,12,14,19,26,58,60,55],\
                  [14,13,16,24,40,57,69,56 ],\
                  [14,17,22,29,51,87,80,62],\
                  [18,22,37,56,68,109,103,77],\
                  [24,35,55,64,81,104,113,92],\
                  [49,64,78,87,103,121,120,101],\
                  [72,92,95,98,112,100,103,99]])

# reading image in grayscale style
fileName = argv[1]

print("> checking if the file " + fileName + " is in /images directory.")

if path.exists("./images/"+fileName) == False:
    print("> file " + fileName + " doesn't exist in /images.")
    exit("non-existence file.")
else:
    print("> image " + fileName + " found.")
    img = cv2.imread("./images/"+fileName, IMREAD_GRAYSCALE)
    print("> image grayscaled.")
    # get size of the image
    [h,w] = img.shape

print("> image size: " + str(h)+"x"+str(w)+".")

# No of blocks needed : Calculation

height = h
width = w
h = np.float32(h) 
w = np.float32(w) 

nbh = math.ceil(h/block_size)
nbh = np.int32(nbh)

nbw = math.ceil(w/block_size)
nbw = np.int32(nbw)


# Pad the image, because sometime image size is not dividable to block size
# get the size of padded image by multiplying block size by number of
# blocks in height/width

# height of padded image
H =  block_size * nbh

# width of padded image
W =  block_size * nbw

# create a numpy zero matrix with size of H,W
print("> writing uncompressed bitmap.")
padded_img = np.zeros((H,W))
padded_img[0:height,0:width] = img[0:height,0:width]
cv2.imwrite('./results/uncompressed.bmp', np.uint8(padded_img))

print("> starts dct transform, uniform quantization, and zig-zag scanning.")
# start encoding:

for i in range(nbh):
    # Compute start and end row index of the block
    row_ind_1 = i*block_size                
    row_ind_2 = row_ind_1+block_size
    
    for j in range(nbw):
        col_ind_1 = j*block_size                       
        col_ind_2 = col_ind_1+block_size
        block = padded_img[row_ind_1:row_ind_2,\
                               col_ind_1:col_ind_2 ]
        DCT = dct(block)            
        DCT_normalized = np.divide(DCT, Q_MAT).astype(int)
        reordered = zigzag(DCT_normalized)
        reshaped= np.reshape(reordered,(block_size, block_size))
        padded_img[row_ind_1:row_ind_2\
                   ,col_ind_1:col_ind_2] = reshaped                        

print("> three tasks done.")
imwrite('./results/encoded.bmp', np.uint8(padded_img))
print("> wrote dct results to new images."\
      + " saved as \"./results/encoded.bmp\".")

#arranged = padded_img.flatten()
print("> getting a bitstream for \"encoded.bmp\"")
bitstream = get_bitstream(padded_img.flatten())
bitstream = str(padded_img.shape[0])\
    + " " + str(padded_img.shape[1]) + " " + bitstream + ";"

print("> writing bitstream to .txt file.")
# Written to image.txt
file1 = open("./results/image.txt","w+")
file1.write(bitstream)
file1.close()

print("> begin converting bitstream to huffman code.")
# new installment (huffman coding)
bitty = bitstream.split()
freq = {}

for i in bitty:
    if i in freq:
        freq[i] += 1
    else:
        freq[i] = 1

freq = sorted(freq.items(),key=lambda x: x[1],reverse=True)
nodes = freq

while len(nodes) > 1:
    (k1,c1) = nodes[-1]
    (k2,c2) = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(k1,k2)
    nodes.append((node, c1 + c2))
    nodes = sorted(nodes,key=lambda x: x[1],reverse=True)

hCode = huffmanCodeTree(nodes[0][0])

print("> finished huffman code.")
print("> writing the finished result to .txt file.")
wr = open("./results/huffman_encode.txt","w")
for i in bitty:
    wr.write(hCode[i])
wr.close()
print("> wrote txt file as \"./results/huffman_encode.txt\".")
print("> writing huffman code tree as \"./results/hufftree.json\".")
json.dump(hCode,open("./results/hufftree.json","w+"))
print("> finished encoding image.")
