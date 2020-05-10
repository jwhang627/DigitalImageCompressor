# src/main.py

import numpy as np
import cv2
import math
from dct import dct_2d
from idct import idct_2d
from skimage.color import rgb2gray
from zigzag import *
from huffman import *

QUANTIZATION_MAT = np.array([[16,11,10,16, 24, 40, 51, 61],\
                             [12,12,14,19, 26, 58, 60, 55],\
                             [14,13,16,24, 40, 57, 69, 56],\
                             [14,17,22,29, 51, 87, 80, 62],\
                             [18,22,37,56, 68,109,103, 77],\
                             [24,35,55,64, 81,104,113, 92],\
                             [49,64,78,87,103,121,120,101],\
                             [72,92,95,98,112,100,103, 99]])

def printing2dArray(a):
    mat = np.asarray(a)
    h,w = a.shape

    for i in range(h):
        for j in range(w):
            if a[i][j] < 0:
                print(round(a[i][j],5),end='| ')
            else:
                print(round(a[i][j],5),end=" | ")
        print("")

def get_bitstream(img):
    i = 0
    skip = 0
    stream = []
    bitstream = ""
    img = img.astype(int)
    
    while (i < img.shape[0]):
        if img[i] != 0:
            stream.append((img[i],skip))
            bitstream += str(img[i]) + " " + str(skip) + " "
            skip = 0
        else:
            skip += 1
        i += 1

    return bitstream
        
def main():
    # bring an image
    fileName = "./images/640-jpeg/empress.jpeg"
    image = cv2.imread(fileName)
    height, width = image.shape[0:2]
    subs = 8
    print("> image name: "+fileName)
    print("> image size: "+str(height)+"x"+str(width))
    
    # resize if the image cannot be divided by "subs"
    if ((height%subs != 0) or (width%subs != 0)):
        height -= height%subs
        width -= width%subs
        image = cv2.resize(image, dsize=(width,height))

    print("> converted image size: " + str(height) + "x" + str(width))

    # creating padded image for encoding
    padded_img = np.zeros([height,width])
    
    # grayscale the image
    img = rgb2gray(image)
    print("> graying the image.")
    for i in range(height):
        for j in range(width):
            img[i][j] = int(round(img[i][j]*255,0))
    cv2.imwrite("./results/gray_image.jpeg",img)
    print("> image grayscaled.")

    padded_img[0:height,0:width] = img[0:height,0:width]
    
    #gray out (subtract 128)
    new_img = np.empty([height,width])
    print("> subtracting gray image with 128.")
    for i in range(height):
        for j in range(width):
            new_img[i][j] = img[i][j] - 128
    cv2.imwrite("./results/gray_image_128.jpeg",new_img)
    print("> subtracted gray image with 128.")
    
    print("> converting them to dct images.")
    for i in range(int(height/subs)):
        for j in range(int(width/subs)):
            dct_2d(img[(0+subs*i):(subs+subs*i),\
                       (0+subs*j):(subs+subs*j)])
            dct_2d(new_img[(0+subs*i):(subs+subs*i),\
                       (0+subs*j):(subs+subs*j)])
            dct_normal = np.divide(\
                        new_img[(0+subs*i):(subs+subs*i),\
                                (0+subs*j):(subs+subs*j)],\
                                   QUANTIZATION_MAT).astype(int)
            reordered = zigzag(dct_normal)
            reshaped = np.reshape(reordered,(subs,subs))
            padded_img[(0+subs*i):(subs+subs*i),\
                       (0+subs*j):(subs+subs*j)]\
                       = reshaped

    cv2.imwrite("./results/reshaped.jpeg",np.uint8(padded_img))
    cv2.imwrite("./results/reshaped.bmp",np.uint8(padded_img))
    # write the dct result
    cv2.imwrite("./results/dct_result.jpeg",img)
    cv2.imwrite("./results/dct_result_128.jpeg",new_img)
    print("> dct convert done.")
    print("> getting a bitstream.")
    bitstream = get_bitstream(padded_img.flatten())
    print("> the compressed image contains " \
          + str(len(bitstream)) + " bits.")

    #writing to bitmap.txt
    file1 = open("./results/bitmap.txt","w+")
    file1.write(bitstream)
    file1.close()
    
    # huffman code
    print("> converting bitstream to huffman code.")
    bitstream = bitstream.split()
    freq = {}
    for c in bitstream:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    nodes = freq
    while len(nodes) > 1:
        (k1,c1) = nodes[-1]
        (k2,c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(k1,k2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    hCode = huffmanCodeTree(nodes[0][0])

    print("> compressing bitstream into binary file.")
    wr = open("./results/binary.bin","w")
    for i in bitstream:
        wr.write(hCode[i])
    wr.close()
    print("> done compressing bitstream into binary file.")

    # decoding it back
    print("> decoding binary file back.")
    open_bin = open("./results/binary.bin","r")
    r_bin = open_bin.read()
    open_bin.close()
    decode = huffmanDecode(r_bin,hCode)
    details = decode.split()
    #print(bitstream[0:8])
    #print(decode.split()[0:8])
    #decode_len = len(decode)
    print("> done decoding.")
    #h_decode, w_decode = decode.split().shape
    #h_decode, w_decode = height, width
    h = int(''.join(filter(str.isdigit,details[0])))
    w = int(''.join(filter(str.isdigit,details[1])))
    #arr = np.zeros([height,width]).astype(int)
    arr = np.zeros(h*w).astype(int)
    #decode.split()
    # some loop var initialization
    """
    a = 0
    b = 1
    for i in range(decode_len):
        arr[a][b-1] = decode[i]
        b += 1
        if (b%width == 0):
            a += 1
            b = 0
    """
    k = 0
    i = 2
    x = 0
    j = 0

    while k < arr.shape[0]:
        if(details[i] == ';'):
            break

        if "-" not in details[i]:
            arr[k] = int(''.join(filter(str.isdigit, details[i])))        
        else:
            arr[k] = -1*int(''.join(filter(str.isdigit, details[i])))        

        if(i+3 < len(details)):
            j = int(''.join(filter(str.isdigit, details[i+3])))

        if j == 0:
            k += 1
        else:
            k += j + 1        

        i += 2

    arr = np.reshape(arr,(h,w))
    print("> converting decoded file to idct image.")

    # loop for constructing intensity matrix form frequency matrix (IDCT)
    padded_img = np.zeros((height,width))
    """
     print("> converting them to dct images.")
    for i in range(int(height/subs)):
        for j in range(int(width/subs)):
            dct_2d(img[(0+subs*i):(subs+subs*i),\
                       (0+subs*j):(subs+subs*j)])
            dct_2d(new_img[(0+subs*i):(subs+subs*i),\
                       (0+subs*j):(subs+subs*j)])
            dct_normal = np.divide(\
                        new_img[(0+subs*i):(subs+subs*i),\
                                (0+subs*j):(subs+subs*j)],\
                                   QUANTIZATION_MAT).astype(int)
            reordered = zigzag(dct_normal)
            reshaped = np.reshape(reordered,(subs,subs))
            padded_img[(0+subs*i):(subs+subs*i),\
                       (0+subs*j):(subs+subs*j)]\
                       = reshaped
    """
    """
    for i in range(int(height/subs)):
        for j in range(int(width/subs)):
            temp_stream = arr[(0+subs*i):(subs+subs*i),\
                              (0+subs*j):(subs+subs*j)]
            block = izigzag(temp_stream.flatten(),subs,subs);
            de_quantized = np.multiply(block,QUANTIZATION_MAT)
            padded_img[(0+subs*i):(subs+subs*i),\
                       (0+subs*j):(subs+subs*j)]\
                       = idct_2d(de_quantized)
            # cv2.idct(de_quantized)
            #idct_2d(padded_img[(0+subs*i):(subs+subs*i),\
            #                   (0+subs*j):(subs+subs*j)])
    """
    i = 0
    j = 0
    k = 0
    while i < h:
        j = 0
        while j < w:
            temp_stream = arr[i:i+8,j:j+8]
            block = izigzag(temp_stream.flatten(), subs, subs)
            de_quantized = np.multiply(block,QUANTIZATION_MAT)
            padded_img[i:i+8,j:j+8] = cv2.idct(de_quantized)
            j += 8
        i += 8
    
    print("> done inverting dct.")
    print("> writing a new compressed bitmap image.")
    padded_img[padded_img > 255] = 255
    padded_img[padded_img < 0] = 0
    # there was an error
    cv2.imwrite("./results/compressed_idct_image.bmp",np.uint8(padded_img))
    print("> done.")
    
if __name__ == '__main__':
    main()
