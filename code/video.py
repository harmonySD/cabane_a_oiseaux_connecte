
from mask import create_mask
cap=cv2.VideoCapture(0)
image_fond = cv2.imread(
    "info_image_oiseaux/image_blanche.jpeg")

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
cap.release()
cv2.destroyAllWindows()

#ouvre la camera 
#prendre photo a partir de ca ? 
# tester avec mask si presence ?
# si presence alors prendre photo et appel blabla 
