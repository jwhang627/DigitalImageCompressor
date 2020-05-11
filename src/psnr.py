# src/psnr.py

# peak signal-to-noise ratio

from math import log10, sqrt
import cv2
import numpy as np

#img1 = cv2.imread("./results/uncompressed.bmp")
#img2 = cv2.imread("./results/compressed_image.bmp")
#psnr = cv2.PSNR(img1,img2)

#print("> psnr value from cv2 library is: " + str(psnr) + "dB.")

def PsnR(ori,com):
    mse = np.mean((ori - com)**2)
    print("> MSE: " + str(mse) + ".")
    if (mse == 0):
        # MSE is zero means no noise is present in the signal .
        # Therefore PSNR have no importance. 
        return 100
    max_pix = 255.0
    p_s_n_r = 20 * log10(max_pix/sqrt(mse))
    return p_s_n_r

def main():
    original = cv2.imread("./results/uncompressed.bmp")
    compressed = cv2.imread("./results/compressed_image.jpeg")
    value = PsnR(original,compressed)
    print("> psnr value between bmp and jpeg" +\
          " from constructed function is: "\
                 + str(value) + " dB.")
    print("> psnr value between bmp and jpeg" +\
          " from cv2 library is: "\
          +str(cv2.PSNR(original,compressed)) + " dB.")
    compressed = cv2.imread("./results/compressed_image.bmp")
    value = PsnR(original,compressed)
    print("> psnr value between two bmps is " + str(value) + " dB.")
    print("> psnr value between two bmps" +\
          " from cv2 library is: "\
          +str(cv2.PSNR(original,compressed)) + " dB.")

if __name__ == "__main__":
    main()
