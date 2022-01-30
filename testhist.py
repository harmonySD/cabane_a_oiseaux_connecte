import cv2
from cv2 import CV_32F
import numpy as np

# importing library for plotting
from matplotlib import pyplot as plt
  
def process(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 0, 50)
    img_dilate = cv2.dilate(img_canny, None, iterations=1)
    img_erode = cv2.erode(img_dilate, None, iterations=0)
    return img_erode

def get_masked(img):
    h, w, _ = img.shape
    center = h // 2, w // 2
    contours, _ = cv2.findContours(process(img), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 100:
            if cv2.pointPolygonTest(cnt, center, False) > 0:
                mask = np.zeros((h, w), 'uint8')
                cv2.drawContours(mask, [cnt], -1, 255, -1)
                return cv2.bitwise_and(img, img, mask=mask)




def create_mask(image, background, threshold):
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    
    image = image.astype(np.int16)
    background = background.astype(np.int16)
    
    # différence entre frame et background
    mask = np.abs(image - background)
    mask = mask.astype(np.uint8)
    
    is_greater_threshold = mask > threshold
    
    # Mettre en blancs les élements qui ont une trop grande différence avec le background
    mask[is_greater_threshold] = 255
    
    # Sinon en noir
    mask[np.logical_not(is_greater_threshold)] = 0
    

    # Nettoyage du mask
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=0)
    mask = cv2.dilate(mask, kernel, iterations=0)
    
    
    return mask

# reads an input image
image_fond=cv2.imread("image_blanche.jpeg")

seuil=10

img = cv2.imread("mesange.jpg")
img1=create_mask(img, image_fond,seuil)


cv2.imshow("Image", img1)
cv2.waitKey(0)
  
# find frequency of pixels in range 0-255
histr = cv2.calcHist([img],[0],img1,[256],[0,256])
  
# show the plotting graph of an image
plt.plot(histr)
plt.show()
