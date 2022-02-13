import cv2

from color_analysis import LoadHistogramsAllFromReferencesBird, tellClosestBird
from enregistrement_resize import enregistre, resize

# ! Résultats des tests
"""
Erreurs de test :
photo 2 => répond moineau au lieu de pigeon
photo 7 => répond moineau au lieu de étourneau
photo 9 => répond moineau au lieu de merles
"""


def main():
    # enregistrer toutes le photos et les redimensionnes
    enregistre("./info_image_oiseaux/images.txt")
    resize("./info_image_oiseaux/images")

    histoRefs = LoadHistogramsAllFromReferencesBird()

    # ? image cible : écris en dure ici pour l'exemple
    img_target = cv2.imread("info_image_oiseaux/images/resizeimage19.jpg")

    #appel comparaison
    tellClosestBird(img_target, histoRefs)


if __name__ == "__main__":
    main()
