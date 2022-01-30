import cv2
import numpy as np
import circleandcenter as circ


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


    
#2 images de meme dimensions
image_fond=cv2.imread("image_blanche.jpeg")
oiseau=cv2.imread("mesange.jpg")

seuil=10

#oiseau en blanc
mask=create_mask(oiseau,image_fond,seuil)
#appel circleandcenter
mask2,rad=circ.get_masked(oiseau)
#appel code.py (pour couleur)

cv2.imshow("mask2",mask2)
cv2.imshow("oiseau",oiseau)
cv2.imshow("mask",mask)
print(rad)

#utiliser tout ca pour determiner l'oiseau avec un tableau avec des oiseaux deja etablis

cv2.waitKey()
#cv2.destroyAllWindows()

