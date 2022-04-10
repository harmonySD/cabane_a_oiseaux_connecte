
import time

import cv2
import numpy as np

from mask import create_mask

cap=cv2.VideoCapture(0)
#image_fond = cv2.imread(
 #   "info_image_oiseaux/image_blanche.jpeg")
time.sleep(5)
frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 
   
size = (frame_width, frame_height) 
   
result = cv2.VideoWriter('filename.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, size) 


img_opti = []

def getSurfaceOfImage(img):
    flattened = [val for pix in img for val in pix]
    return flattened.count(255)
    
# renvoie image avec le plus de pixel blanc
def setOptimalPhoto():
    global img_opti, score
    img_opti = img_list[score.index(max(score))]
    
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

    mask=create_mask(frame,image_fond,15)
    
    cv2.imshow("mask",mask)
    #cv2.imshow('Camera', frame)
    # if cv2.waitKey(1)&0xFF==ord('q'):
    #     break
     #pour changer de fond
    now= time.localtime(time.time())

    # if(int(time.strftime("%S",begin_time))+2<int(time.strftime("%S",now))):     
    #surface = getSurfaceOfImage(mask)
    #     # ? ici 80000 est une valeur arbitrairxwe
    #if surface > 80000 and compteur < 5:
    #         score.append(surface)
    #         img_list.append(frame)
        # compteur += 1
        # print("ici")
    if ret ==True:
        result.write(frame) 
    #         #declencer la capture ?

    #     elif compteur == 5:
    #         print("enfin ...")
    #         setOptimalPhoto()
    #         img_list = []
    #         score = []
    #         compteur = 0
   
    # ! changer le 100 en 10 à la fin des tests 
    print("tour")
    if((int(time.strftime("%S",begin_time))+60<int(time.strftime("%S",now)) )or (int(time.strftime("%M",begin_time))<int(time.strftime("%M",now)))):
        image_fond=new_fond()
        # print(time.strftime("%S",begin_time))
        # print(time.strftime("%S",now))
        print("changement fond")
        begin_time=time.localtime(time.time())
    
cap.release()
result.release()
cv2.destroyAllWindows()
