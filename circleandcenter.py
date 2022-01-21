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
                return img


oiseau=cv2.imread("/Users/harmonysimon-duchatel/M1/blerald-simon-duchatel-2021/cat_01.jpg")
img=get_masked(oiseau)
# convert image to grayscale image
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# convert the grayscale image to binary image
ret,thresh = cv2.threshold(gray_image,127,255,0)


# calculate moments of binary image
M = cv2.moments(thresh)




# calculate x,y coordinate of center
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])



# put text and highlight the center
cv2.circle(img, (cX, cY),5, (255, 0,0 ), 4)
cv2.putText(img, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# display the image
cv2.imshow("Image", img)
cv2.waitKey(0)