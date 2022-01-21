import cv2
import numpy as np

def process(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 0, 50)
    img_dilate = cv2.dilate(img_canny, None, iterations=1)
    img_erode = cv2.erode(img_dilate, None, iterations=1)
    return img_erode

def get_masked(img):
    h, w, _ = img.shape
    center = h // 2, w // 2
    contours, _ = cv2.findContours(process(img), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 100:
            if cv2.pointPolygonTest(cnt, center, False) > 0:
                cnts=contours[0]
                (x,y),radius=cv2.minEnclosingCircle(cnts)
                center = (int(x),int(y))
                radius = int(radius)
                cv2.circle(img,center,radius,(0,255,0),2)
                return img, radius


#pour test
#oiseau=cv2.imread("pigeon.jpg")
#img, rad=get_masked(oiseau)
#print(rad)

#cv2.imshow("Image", img)
#cv2.waitKey(0)