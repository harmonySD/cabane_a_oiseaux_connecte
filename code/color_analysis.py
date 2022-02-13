import cv2
import numpy as np
from cv2 import CV_32F
# importing library for plotting
from matplotlib import pyplot as plt

# global variables
image_fond = cv2.imread("image_blanche.jpeg")
seuil = 10

def process(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 0, 50)
    img_dilate = cv2.dilate(img_canny, None, iterations=1)
    img_erode = cv2.erode(img_dilate, None, iterations=0)
    return img_erode


def get_masked(img):
    h, w, _ = img.shape
    center = h // 2, w // 2
    contours, _ = cv2.findContours(
        process(img), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 100:
            if cv2.pointPolygonTest(cnt, center, False) > 0:
                mask = np.zeros((h, w), 'uint8')
                cv2.drawContours(mask, [cnt], -1, 255, -1)
                return cv2.bitwise_and(img, img, mask=mask)

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
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=0)
    mask = cv2.dilate(mask, kernel, iterations=0)

    return mask

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
            images_list.append(cv2.imread(
                "../ressources/" + bird_name + ".png"))
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
    bird_names = ["merles", "pigeon", "mesanges", "moineau", "pie"]
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

# ? Ou ranger l'image envoyé par le Rapsberry Pi
# ! Tests : A enlever à la fin, il n'y a rien dans ressource pour l'instant
# ! ------------------------------------ 
