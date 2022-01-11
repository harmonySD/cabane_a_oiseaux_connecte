import os
import urllib.request

import cv2
import numpy as np


def enregistrement_image():
    neg_images_link = 'https://images.pexels.com/photos/47547/squirrel-animal-cute-rodents-47547.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260'
      
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    pic_num = 1
    
    if not os.path.exists('neg'):
        os.makedirs('neg')
        
    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.request.urlretrieve(i, "neg/"+str(pic_num)+".jpg")
            img = cv2.imread("neg/"+str(pic_num)+".jpg",cv2.IMREAD_GRAYSCALE)
            # les images négatives doivent être plus grande que les positives pour qu'on puisse placé les positives

            #dessus

            resized_image = cv2.resize(img, (100, 100))

            cv2.imwrite("neg/"+str(pic_num)+".jpg",resized_image)

            pic_num += 1
            
        except Exception as e:
            print(str(e)) 

enregistrement_image()
