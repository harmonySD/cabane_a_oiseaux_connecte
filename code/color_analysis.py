import cv2
import numpy as np
from cv2 import CV_32F
# importing library for plotting
from matplotlib import pyplot as plt

from mask import create_mask


def process(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 0, 50)
    img_dilate = cv2.dilate(img_canny, None, iterations=1)
    img_erode = cv2.erode(img_dilate, None, iterations=0)
    return img_erode


def getDataFromHist(hist):
    hist = hist.flatten()
    total = sum(hist)
 
    data = [(sum(hist[i * 16: (i * 16) + 16])) for i in range(16)]
    return [(data[i] * (100 / total)) for i in range(16)]


def getPourcentageFromData(data1, data2):
    pourcentages = []
    for i in range(16):
        a = data1[i] if data1[i] <= data2[i] else data2[i]
        b = data1[i] if data1[i] > data2[i] else data2[i]

        pourcentages.append(a / b if b != 0 else (a+1) / (b+1))

    return (sum(pourcentages) / 16) * 100


# reads an input image
image_fond = cv2.imread("image_blanche.jpeg")

seuil = 10

img_p = cv2.imread("merle2.jpg")
mask_p = create_mask(img_p, image_fond, seuil)

img_m = cv2.imread("merle.jpg")
mask_m = create_mask(img_m, image_fond, seuil)

histr1 = cv2.calcHist([img_p], [0], mask_p, [256], [0, 256])
data1 = getDataFromHist(histr1)

"""
print("data 1: ", data1)
plt.plot(histr1)
plt.show()
"""

histr2 = cv2.calcHist([img_m], [0], mask_m, [256], [0, 256])
data2 = getDataFromHist(histr2)

"""
print("data 2: ", data2)
plt.plot(histr2)
plt.show()
"""

print("pourcentage : ", getPourcentageFromData(data1, data2))
