import os
import urllib.request

import cv2


def resize(path):
    try:
       files = os.listdir(path) 
       for filename in files:
            filename2="../info_image_oiseaux/images/"+filename
            #lire l'image
            oriimg = cv2.imread(filename2) 
            # redimensionnement de l'image
            newimg = cv2.resize(oriimg,(800, 548))  
            # sauvegarder l'image
            cv2.imwrite("../info_image_oiseaux/images/resize"+filename,newimg)
            #importation de librairie nécessaires 
    except Exception as e:
        print(str(e))


def enregistre(path):
    file = open(path, "r")
    lines = file.readlines()
    file.close()
    nb=0
    for line in lines:
        print("line : ", line)
        url=line
        nom="../info_image_oiseaux/images/image"+str(nb)+".jpg"
        urllib.request.urlretrieve(url, nom)
        nb+=1



