#importation de librairie nécessaires 
import urllib.request
import cv2
import numpy as np
import os

# fonction qui crée le fichier de description pour nos images négatives                
def descripteur():
    for file_type in ['neg']:   
        for img in os.listdir(file_type):
            if file_type == 'neg':
                line = file_type+'/'+img+'\n'
                with open('bg.txt','a') as f:
                    f.write(line)

descripteur()