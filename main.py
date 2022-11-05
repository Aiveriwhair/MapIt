import cv2 as cv
from src.imagegenerator import ImageGenerator
from src.image import Image


# Etapes de la génération d'une image custom
#1- Récupération de l'image maps
ImageGenerator.setup()
ImageGenerator.GenImagebyPlaceName(imageName="img.png",addr="Paris", pregion="", pzoom=13, size=[720, 1080])
map = cv.imread("img.png")

#2- Customization de la map
CustomMap = Image.GenMyCustomMap(
            src=map,
            masksRange=[([250,250,250], [255,255,255], [128,128,128]), ([158,218,238],[176,243,256], [190,190,190])],
            gradientInterval=(1, 1))

#3- Sauvegarde de la nouvelle image
cv.imwrite("treated.jpg", CustomMap)

