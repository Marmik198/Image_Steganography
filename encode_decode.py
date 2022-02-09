import cv2  
import numpy as numpy
from PIL import Image

def intToBinary(rgb):
    r, g, b = rgb
    return ('{0:08b}'.format(r), '{0:08b}'.format(g), '{0:08b}'.format(b))

def binaryToInt(rgb):
    r, g, b = rgb
    return (int(r, 2), int(g, 2), int(b, 2))

def shiftLeft(arr, d):
    newArr = list()
    for i in range(len(arr)):
        temp = arr[i]
        newArr.append(temp[d:] + ("1" * d))
    return newArr

def reduceImageQuality(array):
    reduceArr = list()
    for i in range(len(array)):
        temp = array[i]
        reduceArr.append(temp[0:4] + ("1" * 4))
    return reduceArr

def generateReduceQualityImage():
    image = Image.open("resources/image.png")
    pixelMap = image.load()
    newImage = Image.new(image.mode, image.size)
    newPixelMap = newImage.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            newPixelMap[i, j] = binaryToInt(reduceImageQuality(intToBinary(pixelMap[i, j])))
    newImage.save("resources/reducedQuality.png")

def convertMssgToBinary(messg):
    if type(messg) == str:
        return ''.join([format(ord(i), "08b") for i in messg])
    elif type(messg) == bytes or type(messg) == numpy.ndarray:
        return [format(i, "08b") for i in messg]
    elif type(messg) == int or type(messg) == numpy.uint8:
        return format(messg, "08b")
    else:
        raise TypeError("Input type not supported !!")

def hideData(secretMessage, image):
    totalBytes = image.shape[0] * image.shape[1] * 3 // 8
    print("---------------------------------------------------- ")
    print("Maximum bytes to encode : ", totalBytes)
    if len(secretMessage) > totalBytes:
        raise ValueError("Error, encountered insufficient bytes, need bigger image or less data !!")
    secretMessage += "#####"
    dataIndex = 0
    binarySecretMssg = convertMssgToBinary(secretMessage)
    dataLength = len(binarySecretMssg) 
    for values in image:
        for pixels in values:
            r, g, b = convertMssgToBinary(pixels)
            if dataIndex < dataLength:
                pixels[0] = int(r[:-4] + binarySecretMssg[dataIndex:dataIndex + 4], 2)
                dataIndex += 4
            if dataIndex < dataLength:
                pixels[1] = int(g[:-4] + binarySecretMssg[dataIndex:dataIndex + 4], 2)
                dataIndex += 4
            if dataIndex < dataLength:
                pixels[2] = int(b[:-4] + binarySecretMssg[dataIndex:dataIndex + 4], 2)
                dataIndex += 4
            if dataIndex >= dataLength:
                break
    return image

def generateData(image):
    binaryData = ""
    for values in image:
        for pixels in values:
            r, g, b = convertMssgToBinary(pixels)  
            binaryData += r[-4:]
            binaryData += g[-4:]  
            binaryData += b[-4:] 
            if (binaryData[-40:] == "1111111111111111111111111111111111111111"):
                break
    allBytes = [binaryData[i:i + 8] for i in range(0, len(binaryData), 8)]
    decodedData = ""
    for byte in allBytes:
        decodedData += chr(int(byte, 2))
        if decodedData[-5:] == "#####":
            break
    return decodedData[:-5]

def encodeText():
    imageName = "resources/reducedQuality.png"
    image = cv2.imread(imageName) 
    print("The shape of the image is : ", image.shape)
    file = open('resources/text.txt', 'r')
    data = file.read()
    if (len(data) == 0):
        raise ValueError('Text Data is empty !!')
    fileName = "resources/image_output.png"
    encodedImage = hideData(data, image)  
    cv2.imwrite(fileName, encodedImage)

def decodeText():
    imageName = "resources/image_output.png"
    image = cv2.imread(imageName) 
    text = generateData(image)
    return text

def detectSteganography(image):
    pixelMap = image.load()
    for x in range(1, 5):
        newImage = Image.new(image.mode, image.size)
        newpixelMap = newImage.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            newpixelMap[i, j] = binaryToInt(shiftLeft(intToBinary(pixelMap[i, j]), x))
    newImage.save("resources/detect_steganography/Pixel_bit_shift_left_by_" + str(x) + ".png")

def imageSteganography():
    print("\n---------------------------------------------------- ")
    print("Image Steganography : ")
    print("---------------------------------------------------- ")
    print("1. Encode the data. \n2. Decode the data. \n3. Detect Steganography.")
    print("---------------------------------------------------- ")
    userInput = int(input("Enter your input : "))
    print("---------------------------------------------------- ")
    if (userInput == 1):
        generateReduceQualityImage()
        print("\nEncoding....")
        print("---------------------------------------------------- ")
        encodeText()
        print("---------------------------------------------------- ")
    elif (userInput == 2):
        print("\nDecoding....")
        print("---------------------------------------------------- ")
        print("Decoded message is : \n \n" + decodeText()) 
        print("---------------------------------------------------- ")
    elif (userInput == 3):
        img = Image.open("resources/image_output.png")
        detectSteganography(img)
    else:
        raise Exception("Invalid Input !! Enter correct input (from the above options) !!")

imageSteganography()
