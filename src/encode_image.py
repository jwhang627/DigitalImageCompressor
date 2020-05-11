# src/encode_image.py

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

# Quantization Matrix
Q_MAT = np.array([[16,11,10,16, 24, 40, 51, 61],\
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
    #print(padded_img[0:5,0:5])
    print("> writing uncompressed bitmap.")
    imwrite("./results/uncompressed.bmp",np.uint8(padded_img))

    # subtracting image data with 128
    print("> subtracting bitmap image with 128.")
    img_128 = np.zeros([height,width])
    img_128[0:height,0:width] = image[0:height,0:width]
    for i in range(height):
        for j in range(width):
            img_128[i][j] -= 128

    print("> subtracted bitmap image with 128.")
    print("> writing subtracted bitmap.")
    imwrite("./results/uncompressed_128.bmp",np.uint8(img_128))

    print("> starts dct transform, uniform quantization, and zig-zag scan.")
    for i in range(num_blocks_h):
        row_ind_1 = bl_size * i
        row_ind_2 = row_ind_1 + bl_size
        for j in range(num_blocks_w):
            col_ind_1 = bl_size * j
            col_ind_2 = col_ind_1 + bl_size
            dCT = dct(padded_img[row_ind_1:row_ind_2,col_ind_1:col_ind_2])
            dCT_128 = dct(img_128[row_ind_1:row_ind_2,col_ind_1:col_ind_2])
            dct_norm = np.divide(dCT,Q_MAT).astype(int)
            dct_norm_128 = np.divide(dCT_128,Q_MAT).astype(int)
            reshaped = np.reshape(zigzag(dct_norm),(bl_size,bl_size))
            reshaped_128 = np.reshape(zigzag(dct_norm_128),(bl_size,bl_size))
            padded_img[row_ind_1:row_ind_2,col_ind_1:col_ind_2] = reshaped
            img_128[row_ind_1:row_ind_2,col_ind_1:col_ind_2] = reshaped_128

    print("> three tasks done.")
    print("> writing dct results to new images.")
    imwrite("./results/dct_result.bmp",np.uint8(padded_img))
    #imwrite("./results/dct_result.bmp",padded_img)
    imwrite("./results/dct_result_128.bmp",np.uint8(img_128))
    #imwrite("./results/dct_result_128.bmp",img_128)
    
    # get bitstreams
    print("> get bitstream for \"dct_result.bmp\".")
    bitstr = get_bitstream(padded_img.flatten().astype(int))
    print("> this compressed image contains "\
          + str(len(bitstr)) + " bits.")
    print("> get bitstream for \"dct_result_128.bmp\".")
    bitstr_128 = get_bitstream(img_128.flatten().astype(int))
    print("> this compressed image contains "\
          + str(len(bitstr_128)) + " bits.")
    
    # two terms are assigned for size as well
    bitstr = str(padded_img.shape[0]) + " " + str(padded_img[1]) + " " + bitstr + ";"
    bitstr_128 = str(img_128.shape[0]) + " " + str(img_128.shape[1]) + " " + bitstr_128 + ";"
    
    # writing bitstream to bin and txt file
    print("> writing bitstream to .bin file and .txt file.")
    bitBin = open("./results/binary.bin","w+")
    bitBin.write(bitstr)
    bitBin.close()
    bitTxt = open("./results/bitmap.txt","w+")
    bitTxt.write(bitstr)
    bitTxt.close()

    print("> writing subtracted bitstream to .bin file and .txt file.")
    bitBin = open("./results/binary_128.bin","w+")
    bitBin.write(bitstr_128)
    bitBin.close()
    bitTxt = open("./results/bitmap_128.txt","w+")
    bitTxt.write(bitstr_128)
    bitTxt.close()
    
    #huffman encoding
    print("> begin compressing bitstream stuffs through huffman code.")
    bitty = bitstr.split()
    bitty_128 = bitstr_128.split()
    freq = {}
    freq_128 = {}

    for i in bitty:
        if i in freq:
          freq[i] += 1
        else:
          freq[i] = 1

    for i in bitty_128:
        if i in freq_128:
          freq_128[i] += 1
        else:
          freq_128[i] = 1
          
    freq = sorted(freq.items(),key=lambda x: x[1], reverse=True)
    freq_128 = sorted(freq_128.items(),key=lambda x: x[1], reverse=True)
    nodes = freq
    nodes_128 = freq_128

    while len(nodes) > 1:
        (k1,c1) = nodes[-1]
        (k2,c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(k1,k2)
        nodes.append((node,c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    while len(nodes_128) > 1:
          (k1,c1) = nodes_128[-1]
          (k2,c2) = nodes_128[-2]
          nodes_128 = nodes_128[:-2]
          node = NodeTree(k1,k2)
          nodes_128.append((node,c1 + c2))
          nodes_128 = sorted(nodes_128,key=lambda x: x[1], reverse=True)
          
    hCode = huffmanCodeTree(nodes[0][0])
    hCode_128 = huffmanCodeTree(nodes_128[0][0])
    print("> finished huffman code.")
    print("> writing them to different binary files.")
    wr = open("./results/bitstream.bin","w+")
    for i in bitty:
        wr.write(hCode[i])
    wr.close()
    wr = open("./results/bitstream_128.bin","w+")
    for i in bitty_128:
          wr.write(hCode_128[i])
    wr.close()
    print("> wrote binary files as \"./results/bitstream.bin\" & \"./results/bitstream_128.bin\".")

    # writing json file
    print("> writing huffman node trees as \"./results/hufftree.json\" & \"./results/hufftree_128.json\".")
    json.dump(hCode,open("./results/hufftree.json","w+"))
    json.dump(hCode_128,open("./results/hufftree_128.json","w+"))
          
    #with open("./results/hufftree.pkl","wb") as tree_file:
    #    pickle.dump(hCode,tree_file,pickle.HIGHEST_PROTOCOL)
    #tree_file.close()
    print("> finished encoding images.")

if __name__ == '__main__':
    main()
