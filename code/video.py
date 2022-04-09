import cv2
import time
from mask import create_mask
cap=cv2.VideoCapture(0)
#image_fond = cv2.imread(
 #   "info_image_oiseaux/image_blanche.jpeg")
time.sleep(5)

def new_fond():
    ret, image_fond=cap.read()#mask erode mask dilate dans create_mask pour faire moins precie et gere la
#variation de lumiere 
    cv2.imshow("fond",image_fond)
    return image_fond

#pour cqhanger de fond toute les 10 minutes
image_fond=new_fond()
begin_time= time.localtime(time.time())
while True: 
    ret, frame=cap.read()
    mask=create_mask(frame,image_fond,10)
    cv2.imshow("mask",mask)
    cv2.imshow('Camera', frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
    if cv2.waitKey(1)&0xFF==ord('p'):
        ret, pic=cap.read()
        cv2.imshow("pic",pic)
     #pour changer de fond
    now= time.localtime(time.time())
   
    if(int(time.strftime("%S",begin_time))+10<int(time.strftime("%S",now))):
        image_fond=new_fond()
        print(time.strftime("%S",begin_time))
        print(time.strftime("%S",now))
        begin_time=time.localtime(time.time())
    
cap.release()
cv2.destroyAllWindows()

#ouvre la camera 
#prendre photo a partir de ca ? 
# tester avec mask si presence ?
# si presence alors prendre photo et appel blabla 
# detecter si presence sur masque et prendre photo
# chercher fct qui enregistre el flux video 
# et enregistrer que si presence detecter

