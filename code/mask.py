import cv2
import numpy as np


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
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=5)


    return mask



