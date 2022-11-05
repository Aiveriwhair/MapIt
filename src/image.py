from turtle import color
import cv2 as cv
from cv2 import bitwise_and
import numpy as np
import copy

class Image():

    @staticmethod
    def showImage(windowName, image):
        while(1):
            cv.imshow(windowName, image)
            k = cv.waitKey(5) & 0xFF
            if k == 27:
                break
        cv.destroyAllWindows()


    @staticmethod
    def LaplacianAffutage(src, ddepth):
        return cv.Laplacian(src,ddepth=ddepth, dst=src)



    # Function changeColor
    # Transform all the pixels that has the old color with the newColor specified
    # @params
    # oldColor (b, g, r)
    # newColor (b, g, r)
    # @returns Img
    @staticmethod
    def changeColorSup(image, minRGB, newColor):
        minRGB = np.array(minRGB)
        newColor = np.array(newColor)
        if not minRGB.all() and not newColor.all():
            print('You must to specify both old and new color in function : @changeColorSup')
            quit()
        res = copy.copy(image)
        res[np.where((image >= minRGB).all(axis=2))] = newColor
        return res

    @staticmethod
    def changeColorInf(image, maxRGB, newColor):
        maxRGB = np.array(maxRGB)
        newColor = np.array(newColor)
        if not maxRGB.all() and not newColor.all():
            print('You must to specify both old and new color in function : @changeColorInf')
            quit()
        res = copy.copy(image)
        res[np.where((image <= maxRGB).all(axis=2))] = newColor
        return res

    @staticmethod
    def changeColorEq(image, oldColorRGB, newColor):
        oldColorRGB = np.array(oldColorRGB)
        newColor = np.array(newColor)
        if not oldColorRGB.all() and not newColor.all():
            print('You must to specify both old and new color in function : @changeColorEq')
            quit()
        res = copy.copy(image)
        res[np.where((res == oldColorRGB).all(axis=2))] = newColor
        return res



    @staticmethod
    def GenMaskFromImg(image, LowerColorArray, HigherColorArray):
        lowColor = np.array(LowerColorArray)
        highColor = np.array(HigherColorArray)
        return cv.inRange(image, lowColor, highColor)


    @staticmethod
    def GenLinearGradientMask(image, FadeVal1, FadeVal2): #fades from FadeVal1 to FadeVal2
        CenterX = int(image.shape[1]/2)

        #verticalGradientArray1 = np.linspace(FadeVal2, FadeVal1, CenterY)
        #verticalGradientArray2 = np.linspace(FadeVal1, FadeVal2, CenterY)
        #VerticalGradient = np.concatenate([verticalGradientArray1, verticalGradientArray2])

        horizontalGradientArray1 = np.linspace(FadeVal2, FadeVal1, CenterX)
        horizontalGradientArray2 = np.linspace(FadeVal1, FadeVal2, CenterX)
        HorizontalGradient = np.concatenate([horizontalGradientArray1, horizontalGradientArray2])

        maskHorizontal = np.repeat(np.tile(HorizontalGradient, (image.shape[0], 1))[:,:, np.newaxis], 3, axis=2)
        #maskVertical = np.repeat(np.tile(VerticalGradient, (image.shape[1], 1))[:,:, np.newaxis], 3, axis=2)
        mask = maskHorizontal #+ maskVertical
        return mask


    @staticmethod
    def GenColoredBG(image, colorList):
        ColoredBG = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)
        ColoredBG[:] = colorList
        return ColoredBG





    # Function @GenMyCustomMap
    # @params
    #   @src : description : The source image to Custom 
    #        : type : opencv image
    #   @masks : description : List of mask we want to be applied to the source image 
    #          : The mask will be zeros everywhere except where the source image pixel's
    #          : brg values are within the specified range of value specified. There, it will be 1.
    #          : The mask are then sumed up together
    #          : type : list of tuples of bgr colors
    #       masks = [
    #           ([235,235,235],[255,255,255],[BGRCOLOR1]),
    #           ([[158,218,238],[176,243,256],[BGRCOLOR2]]),
    #           ....
    #           ]
    #   @bgColor : description : The bgr color for the color of the mask
    #            : type : list of 3 values
    #   @gradientInterval : description : Key values for gradient generation
    #                     : type : tuple or list of 2 values within the [0, 1] range
    # @returns :
    #   the Custom map image
    def GenMyCustomMap(src, masksRange=None, gradientInterval=(1,0)):
        if not masksRange :
            return src

        res = np.zeros((src.shape[0],src.shape[1],3), dtype=np.uint8)
        #1- Génération des masks Range
        for maskRange in masksRange:
            #Récupération du mask
            mask = Image.GenMaskFromImg(src, maskRange[0], maskRange[1])
            #Récupération de la couleur
            ColoredBG = Image.GenColoredBG(src, maskRange[2])
            #Application de la couleur
            ColoredMask = bitwise_and(ColoredBG, ColoredBG, mask=mask)
            #Ajout au tableau ColoredMasks
            res += ColoredMask

        #Génération du mask Gradient
        #CustomMask = Image.GenLinearGradientMask(src, gradientInterval[0], gradientInterval[1])
        

        #res = res * CustomMask/255
        return res

    @staticmethod
    def printShape(image):
        print("height : ", image.shape[0],"width : ", image.shape[1], "channels :", image.shape[2])
