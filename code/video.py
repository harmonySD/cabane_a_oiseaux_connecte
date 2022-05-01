
import time

import cv2
import numpy as np

from color_analysis import LoadHistogramsAllFromReferencesBird, tellClosestBird
from enregistrement_resize import enregistre, resize
from mask import create_mask

cap=cv2.VideoCapture('videos/mesange2.mp4')

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
prev = 0
frame_rate = 1      

while True: 
    ret, frame=cap.read()
    mask=create_mask(frame,image_fond,50)
    
    cv2.imshow("mask",mask)
    cv2.imshow('Camera', frame)

    if cv2.waitKey(1)&0xFF==ord('q'):
        break

    # pour changer de fond
    now= time.localtime(time.time())
    time_elapsed = time.time() - prev

    if time_elapsed > 1./frame_rate:
        prev = time.time()
        surface = getSurfaceOfImage(mask)

        # ? ici 80000 est une valeur arbitraire
        if surface > 100 and compteur < 5:
            score.append(surface)
            img_list.append(frame)
            compteur += 1
            print("ici")
            if ret == True:
                result.write(frame) 
        elif compteur == 5:
            print("enfin ...")
            setOptimalPhoto()
            cv2.imshow('img_opti',img_opti)
            
            histoRefs = LoadHistogramsAllFromReferencesBird()
            img_opti = cv2.resize(img_opti,(800, 548))
            #appel comparaison
            tellClosestBird(img_opti, histoRefs)
            
            img_list = []
            score = []
            compteur = 0
            
        print("surface : ",surface)
        print("tour")
        print("time_elapsed : ",time_elapsed)     
        
    # ! changer le 100 en 10 à la fin des tests 
    if((int(time.strftime("%S",begin_time))+60<int(time.strftime("%S",now)) )or (int(time.strftime("%M",begin_time))<int(time.strftime("%M",now)))):
        image_fond=new_fond()
        # print(time.strftime("%S",begin_time))
        # print(time.strftime("%S",now))
        print("changement fond")
        begin_time=time.localtime(time.time())
    
cap.release()
result.release()
cv2.destroyAllWindows()
