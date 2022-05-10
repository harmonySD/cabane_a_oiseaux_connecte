import cv2

from color_analysis import LoadHistogramsAllFromReferencesBird, tellClosestBird
from enregistrement_resize import enregistre, resize

# ! Résultats des tests

def main():
    # enregistrer toutes le photos et les redimensionnes
    enregistre("./info_image_oiseaux/images.txt")
    resize("./info_image_oiseaux/images")

if __name__ == "__main__":
    main()
