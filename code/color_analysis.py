import os
from functools import cmp_to_key

import cv2
import numpy as np
from cv2 import CV_32F
# importing library for plotting
from matplotlib import pyplot as plt

from mask import create_mask

# global variables
image_fond = cv2.imread(
    "info_image_oiseaux/image_blanche.jpeg")
seuil = 10
birds = {"pigeon": 0, "étourneau": 1, "merles": 2, "mesanges": 3, "moineau": 4}


def getDataFromHist(hist):
    hist = hist.flatten()
    total = sum(hist)

    data = [(sum(hist[i * 16: (i * 16) + 16])) for i in range(16)]
    return [(data[i] * (100 / total)) for i in range(16)]


def getPourcentageFromData(data1, data2):
    pourcentages = []
    for i in range(16):
        a = data1[i] if data1[i] <= data2[i] else data2[i]
        b = data1[i] if data1[i] > data2[i] else data2[i]

        pourcentages.append(a / b if b != 0 else (a+1) / (b+1))

    return (sum(pourcentages) / 16) * 100


def getAllImagesFromReferenceBird(bird_name):
    index = birds[bird_name]
    try:
        return [cv2.imread("info_image_oiseaux/images/resizeimage" + str(i) + ".jpg") for i in range((index * 4), (index * 4) + 4)]
    except Exception as e:
        print(e)


def getAllMaskFromReferenceBird(images_list):
    return [create_mask(images_list[i], image_fond, seuil) for i in range(len(images_list))]


def getAllHistogrammesFromReferenceBird(bird_name):
    images_list = getAllImagesFromReferenceBird(bird_name)
    #print('image_list : ',len(images_list), "\n", images_list[0])
    mask_list = getAllMaskFromReferenceBird(images_list)

    return [cv2.calcHist([images_list[i]], [0], mask_list[i], [256], [0, 256]) for i in range(len(images_list))]


def LoadHistogramsAllFromReferencesBird():
   return [getAllHistogrammesFromReferenceBird(list(birds.keys())[i]) for i in range(5)]


# * compare hist_target les 4 hist de l'oiseaux de référence
def compareTargetAndOneReferenceBirds(histTarget, hist_list):
    pourcentages = []
    dataTarget = getDataFromHist(histTarget)

    for histRef in hist_list:
        dataRef = getDataFromHist(histRef)
        pourcentages.append(getPourcentageFromData(dataTarget, dataRef))

    return max(pourcentages)


def compareTargetToAllReferenceBird(hist_target, hist_list):

    pourcentages = [compareTargetAndOneReferenceBirds(
        hist_target, hist_list[i]) for i in range(len(birds))]

    max_value = max(pourcentages)
    max_index = pourcentages.index(max_value)

    return (list(birds.keys())[max_index], pourcentages[max_index])


def tellClosestBird(img_target, hist_list):
    print("width : ", len(img_target))
    print("height : ", len(img_target[0]))
    mask_target = create_mask(img_target, image_fond, seuil)
    hist_target = cv2.calcHist([img_target], [0], mask_target, [256], [0, 256])

    bird = compareTargetToAllReferenceBird(hist_target, hist_list)

    print("D'après une analyse basé strictement sur la couleur, l'oiseau le plus proche de l'oiseau cible est un : ",
          bird[0], ", avec une ressemblance de ", bird[1])


"""
images_test : la photo de l'oiseau de la cabane
images : images oiseaux référence
"""
