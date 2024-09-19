# imports

# PIL Libraries
import PIL
import PIL.Image
import PIL.ImageOps
import PIL.ImageFilter

# OpenCV
import cv2

# KERAS
import keras
from keras import models

# matplot and numpy
import numpy as np
import matplotlib.pyplot as mpl

def downscale_and_crop(img):    
    # Find the minimum dimension of the image
    min_dimension = min(img.size)
    
    # Center crop the image to a square using the minimum dimension
    left = (img.width - min_dimension) / 2
    top = (img.height - min_dimension) / 2
    right = (img.width + min_dimension) / 2
    bottom = (img.height + min_dimension) / 2

    img_cropped = img.crop((left, top, right, bottom))
    
    # Resize the cropped image to 28x28 pixels
    img_resized = img_cropped.resize((28, 28))
    return img_resized



def needToInvert(img, thrshld):
    is_light = np.mean(img) > thrshld
    return True if is_light else False

def invert(img):
    img = PIL.ImageOps.invert(img)
    return img

def center_subject(image_path):
    # Open the image
    img = PIL.Image.open(image_path)

    # Convert image to grayscale (to make edge detection simpler)
    gray_img = PIL.ImageOps.grayscale(img)

    # Apply edge detection filter to highlight subject
    edges = gray_img.filter(PIL.ImageFilter.FIND_EDGES)

    # Get the bounding box of the non-black regions (i.e., where there is content/edges)
    bbox = edges.getbbox()

    # If a bounding box was found, crop the image to this bounding box
    if bbox:
        img_cropped = img.crop(bbox)
    else:
        img_cropped = img  # No edges found, return the original image

    # Get the size of the cropped image
    cropped_width, cropped_height = img_cropped.size

    # Calculate the amount of padding to add to center the subject
    max_side = max(cropped_width, cropped_height)

    # Create a new square image with a white background
    centered_img = PIL.Image.new("RGB", (max_side, max_side), "white")

    # Paste the cropped image into the center of the square image
    offset_x = (max_side - cropped_width) // 2
    offset_y = (max_side - cropped_height) // 2
    centered_img.paste(img_cropped, (offset_x, offset_y))

    # Save the resulting centered image

    return centered_img

#import an image, can be replaced with an loop to go through each item in folder
centeredIMG = center_subject("testIMG/h.jpg")
imgInQuestion = downscale_and_crop(centeredIMG)

if needToInvert(imgInQuestion, 137):
    imgInQuestion = invert(imgInQuestion.convert('RGB'))


# normalized image initialzing
# ONLY NEEDED FOR TESTING
normalizedIMG = PIL.Image.new(mode="RGB", size=(28, 28))

pixelVals = []

image1 = []
# sets all rgb values from 0-255
for y in range(28):
    #row = []
    for x in range(28):
        pixel_rgb = imgInQuestion.getpixel((x, y)) # x, y are the coordinates of the pixel
        avg = float ((pixel_rgb[0] + pixel_rgb[1] + pixel_rgb[2]) / 3)

        # takes img and blackens any values that 
        if (avg < 32):
            avg = 0
        elif (avg < 60):
            avg = 40
        elif (avg > 200):
            avg = 230
        elif (avg > 230):
            avg = 255
        # NEW PIXEL STATEMENTS FOR CREATING NEW IMAGE
        newPixel = (int(avg), int(avg), int(avg))
        normalizedIMG.putpixel((x,y), newPixel)

        # 2D SHAPE OF NORMALIZED VALUES
        #row.append(avg)
        image1.append(avg)
    #pixelVals.append(row)
pixelVals.append(image1)



# STATEMENTS FOR TESTING NORMALIZATION
normalizedIMG.save("normalized.jpg")
# print(pixelVals)
# mpl.matshow(pixelVals)
# mpl.show()

# WORKING WITH MODEL
model = models.load_model('my_model.keras')
print("loaded model")

# reshape and scale array
npPixelVals = np.array(pixelVals)

npPixelVals = npPixelVals/255.0
prediction = model.predict(npPixelVals)


print(prediction.argmax())