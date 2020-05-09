# src/main.py

import numpy as np
import cv2
from dct import dct_2d
from idct import idct_2d
from skimage.color import rgb2gray

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
    fileName = "./images/640-jpeg/empress.jpeg"
    image = cv2.imread(fileName)
    height, width = image.shape[0:2]
    subs = 8
    print("> image name: "+fileName)
    print("> image size: " + str(height) + "x" + str(width))
    
    # resize if the image cannot be divided by "subs"
    if ((height%subs != 0) or (width%subs != 0)):
        height -= height%subs
        width -= width%subs
        image = cv2.resize(image, dsize=(width,height))

    # grayscale the image
    img = rgb2gray(image)
    print("> graying the image.")
    for i in range(height):
        for j in range(width):
            img[i][j] = img[i][j]*256
    cv2.imwrite("./results/gray_image.jpeg",img)
    print("> image grayscaled.")
    print("> converting it to dct image.")
    for i in range(int(height/subs)):
        for j in range(int(width/subs)):
            #printing2dArray(img[(0+8*i):(8+8*i),(0+8*j):(8+8*j)])
            dct_2d(img[(0+subs*i):(subs+subs*i),\
                       (0+subs*j):(subs+subs*j)])

    # write the dct result
    cv2.imwrite("./results/dct_result.jpeg",img)
    print("> dct convert done.")
    # placeholder    
    """
    mat = [[0.50194745, 0.49018275, 0.47725725, 0.46862549, 0.45290941,\
        0.4350051 , 0.43081569, 0.42887412],\
       [0.46051373, 0.02358902, 0.4635651 , 0.44141255, 0.42068784,\
        0.40183922, 0.41215373, 0.41571804],\
       [0.07517176, 0.04688039, 0.03988549, 0.41335843, 0.38008039,\
        0.36972275, 0.37494   , 0.37234275],\
       [0.13759647, 0.03312863, 0.08530745, 0.39096   , 0.58602392,\
        0.57291294, 0.39918863, 0.32116784],\
       [0.2764302 , 0.0634298 , 0.25738745, 0.00306549, 0.67894471,\
        0.61654118, 0.60647294, 0.38092863],\
       [0.51086275, 0.51673373, 0.52673216, 0.61369804, 0.59974588,\
        0.58464   , 0.43445451, 0.63641686],\
       [0.50390588, 0.51188275, 0.4984698 , 0.43199922, 0.51416392,\
        0.5098    , 0.53652471, 0.46000078],\
       [0.53030824, 0.54972941, 0.5470051 , 0.49757255, 0.7049749 ,\
        0.70050275, 0.70857608, 0.64030078]]

    a = dct_2d(mat)
    printing2dArray(a)
    """
    
if __name__ == '__main__':
    main()
