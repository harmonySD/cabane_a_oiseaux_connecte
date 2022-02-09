import cv2
import numpy as np
from cv2 import CV_32F
# importing library for plotting
from matplotlib import pyplot as plt


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
    print(total)

    data = [(sum(hist[i * 16: (i * 16) + 16])) for i in range(16)]
    return [(data[i] * (100 / total)) for i in range(16)]


def getPourcentageFromData(data1, data2):
    pourcentages = []
    for i in range(16):
        a = data1[i] if data1[i] <= data2[i] else data2[i]
        b = data1[i] if data1[i] > data2[i] else data2[i]

        pourcentages.append(a / b if b != 0 else (a+1) / (b+1))

    return (sum(pourcentages) / 16) * 100


# reads an input image
image_fond = cv2.imread("image_blanche.jpeg")

seuil = 10

img_p = cv2.imread("merle2.jpg")
mask_p = create_mask(img_p, image_fond, seuil)

img_m = cv2.imread("merle.jpg")
mask_m = create_mask(img_m, image_fond, seuil)

histr1 = cv2.calcHist([img_p], [0], mask_p, [256], [0, 256])
data1 = getDataFromHist(histr1)
print("data 1: ", data1)
plt.plot(histr1)
plt.show()

histr2 = cv2.calcHist([img_m], [0], mask_m, [256], [0, 256])
data2 = getDataFromHist(histr2)
print("data 2: ", data2)
plt.plot(histr2)
plt.show()

print("pourcentage : ", getPourcentageFromData(data1, data2))
