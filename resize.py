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
        img = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
        # redimensionnement de l'image
        newimg = cv2.resize(img,(100, 100))  
        # afficher l'image
        #cv2.imshow("Show by CV2",newimg)
        #cv2.waitKey(0)
        if not os.path.exists('neg'):
            os.makedirs('neg')
        # sauvegarder l'image
        cv2.imwrite("neg/"+nom + ".jpg",newimg)
        #importation de librairie nécessaires 


    #fonction qui enregistre les images et les numérotes

    except Exception as e:
        print(str(e))

resize("cerf")
resize("chevre")
resize("chien")
resize("elephant")
resize("faucon")
resize("gnou")
resize("grizzly")
resize("guepard")
resize("hamster")
resize("lama")
resize("lion")
resize("marmotte")
resize("panda")
resize("poisson")
resize("racoon")
resize("renard")
resize("serpent")
resize("singe")
resize("singe")
resize("taureau")
resize("zebra")
resize("zemmour")