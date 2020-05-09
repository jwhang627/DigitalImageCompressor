# src/main.py

import numpy as np
import cv2
from dct import dct_2d
from idct import idct_2d
from skimage.color import rgb2gray
from zigzag import *

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
    
def main():
    # bring an image
    fileName = "./images/png/holo.png"
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
    
    
if __name__ == '__main__':
    main()
