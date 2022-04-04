
import time
import typing
from typing import List

import cv2
import numpy as np

from mask import create_mask

cap=cv2.VideoCapture(0)
#image_fond = cv2.imread(
 #   "info_image_oiseaux/image_blanche.jpeg")
time.sleep(5)

img_opti = []

def getSurfaceOfImage(img : np.ndarray) -> int:
    flattened = [val for pix in img for val in pix]
    return flattened.count(255)
    
# renvoie image avec le plus de pixel blanc
def setOptimalPhoto():
    global img_opti, score
    print('score : ',score)
    print('max : ',max(score))
    print('index : ',img_list.index(max(score)))
    img_opti = img_list[img_list.index(max(score))]
    
def new_fond():
    ret, image_fond=cap.read()#mask erode mask dilate dans create_mask pour faire moins precie et gere la
#variation de lumiere 
    cv2.imshow("fond",image_fond)
    return image_fond

#pour changer de fond toute les 10 minutes
image_fond=new_fond()
begin_time= time.localtime(time.time())
compteur = 0
img_list = []
score = []

while True: 
    ret, frame=cap.read()
    mask=create_mask(frame,image_fond,50)
    surface = getSurfaceOfImage(mask)
    print(surface)
    if surface > 80000 and compteur < 100:
        score.append(surface)
        compteur += 1
    elif compteur == 100:
        setOptimalPhoto()
        cv2.imshow("test",img_opti)
        img_list = []
        score = []
        compteur = 0

    cv2.imshow("mask",mask)
    cv2.imshow('Camera', frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
    if cv2.waitKey(1)&0xFF==ord('p'):
        ret, pic=cap.read()
        cv2.imshow("pic",pic)
     #pour changer de fond
    now= time.localtime(time.time())
   
    if(int(time.strftime("%S",begin_time))+100<int(time.strftime("%S",now))):
        image_fond=new_fond()
        print(time.strftime("%S",begin_time))
        print(time.strftime("%S",now))
        begin_time=time.localtime(time.time())
    
cap.release()
cv2.destroyAllWindows()
