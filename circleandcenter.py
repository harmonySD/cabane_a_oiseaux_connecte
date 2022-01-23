import re
import cv2
import numpy as np

def process(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 0, 50)
    img_dilate = cv2.dilate(img_canny, None, iterations=2) #sinon marche pas avec 1 ! It is also useful in joining broken parts of an object.
    img_erode = cv2.erode(img_dilate, None, iterations=1)
    return img_erode



def get_masked(img):
    #evite d'ecrire sur photo principal
    newimg=img.copy()
    h, w, _ = img.shape
    center = h // 2, w // 2
    contours, _ = cv2.findContours(process(newimg), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    (x,y),radius=cv2.minEnclosingCircle(contours[0])
    center = (int(x),int(y))
    radius = int(radius)

    cv2.circle(newimg,center,radius,(0,255,0),2)

    return newimg,radius

#pour test
#oiseau=cv2.imread("moineau.jpg")
#img, rad =get_masked(oiseau)
#print(rad)


#cv2.imshow("Image", oiseau)
#cv2.waitKey(0)