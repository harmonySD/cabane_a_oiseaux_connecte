from enregistrement_resize import resize
from enregistrement_resize import enregistre


def main():
    # enregistrer toutes le photos et les redimensionées
    enregistre("../info_image_oiseaux/images.txt")
    resize("../info_image_oiseaux/images")


    #pour chaque image appel histogramme ?

    #appel comparaison


    


if __name__ == "__main__":
    main()
