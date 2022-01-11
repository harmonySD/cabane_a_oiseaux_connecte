import os
import urllib.request

import cv2
import numpy as np


def resize(nom):
    try:
        # entrer le nom du fichier de l'image
        filename = "images/" + nom + ".jpg"  
        #lire l'image
        oriimg = cv2.imread(filename) 
        # redimensionnement de l'image
        newimg = cv2.resize(oriimg,(50, 50))  
        # afficher l'image
        cv2.imshow("Show by CV2",newimg)
        cv2.waitKey(0)
        # sauvegarder l'image
        cv2.imwrite(nom + ".jpg",newimg)
        #importation de librairie nécessaires 


    #fonction qui enregistre les images et les numérotes

    except Exception as e:
        print(str(e))

resize("marmotte")
