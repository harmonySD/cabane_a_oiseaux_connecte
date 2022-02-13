import cv2
import numpy as np
from cv2 import CV_32F
# importing library for plotting
from matplotlib import pyplot as plt

from mask import create_mask

# global variables
image_fond = cv2.imread("image_blanche.jpeg") # * changer le path
seuil = 10

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

# work if image ard named : bird_name + 1.format and format is either png or jpg
def getAllImagesFromReferenceBird(bird_name):
    images_list = []
    for i in range(5):
        try:
            images_list.append(cv2.imread(
                "../ressources/" + bird_name + ".jpg"))
        except Exception:
            print()
            raise 
    return images_list


def getAllMaskFromReferenceBird(bird_name, images_list):
    return [create_mask(images_list[i], image_fond, seuil) for i in range(len(images_list))]


def getAllHistogrammesFromReferenceBird(bird_name):
    images_list = getAllImagesFromReferenceBird(bird_name)
    mask_list = getAllMaskFromReferenceBird(bird_name, images_list)

    return [cv2.calcHist([images_list[i]], [0], mask_list[i], [256], [0, 256]) for i in range(len(images_list))]


def compareTargetAndOneReferenceBirds(histTarget, hist_list):
    pourcentages = []
    dataTarget = getDataFromHist(histTarget)

    for histRef in hist_list:
        dataRef = getDataFromHist(histRef)
        pourcentages.append(getPourcentageFromData(dataTarget, dataRef))

    return sum(pourcentages) / len(pourcentages)


def compareTargetToAllReferenceBird(hist_target):
    bird_names = ["merles", "pigeon", "mesanges", "moineau", "étourneau"]
    pourcentages = [compareTargetAndOneReferenceBirds(
        hist_target, name) for name in bird_names]

    max_value = max(pourcentages)
    max_index = pourcentages.index(max_value)
    return (bird_names[max_index], pourcentages[max_index])


def tellClosestBird(img_target):
    mask_target = create_mask(img_target, image_fond, seuil)
    hist_target = cv2.calcHist([img_target], [0], mask_target, [256], [0, 256])

    bird = compareTargetToAllReferenceBird(hist_target)

    print("D'après une analyse basé strictement sur la couleur, l'oiseau le plus proche de l'oiseau cible est  un : ",
          bird[0], " avec une ressemblance de ", bird[1])

# ? Ou ranger l'image envoyé par le Rapsberry Pi => info_image_oiseaux
# ! ------------------------------------ 

"""
images_test : la photo de l'oiseau de la cabane
images : images oiseaux référence
"""
