# Image_Steganography

## Steps to encode, detect & decode

1.  Clone this git repository
    
    encode\_decode.py - <br>
        1. Encodes and Decodes the text into/from image.<br>
        2. Detects the image steganography by left shifting the pixel RGB value.

![](readme_image/image7.png)


2.  Copy image.png(original) and text.txt(text to hide) to resources folder

![](readme_image/image5.png)

3.  Text will be converted to binary and will be encoded to image by dropping 4 LSB of image pixel bits value and copying text binary value in place.

![](readme_image/image1.png)


4.  Running script to encode the text into image

![](readme_image/image6.png)

5.  “image\_output.png“ (image with text hidden) will be generated in the resources folder.

![](readme_image/image2.png)

6.  Analysing the image to detect steganography

![](readme_image/image4.png)


7.  Image will be generated in detect\_steganography folder

![](readme_image/image3.png)

8.  Encoded text is visible in the image after 4 bit left shift of pixels

![](readme_image/image9.png)

9.  Decoding the text from image

![](readme_image/image8.png)
