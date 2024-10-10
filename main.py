import mnistPrediction as mp
import os


directory = 'testIMG'


for filename in os.listdir(directory):
    imgPath = os.path.join(directory, filename)
    if os.path.isfile(imgPath):
        print("File: " + imgPath + " \nPredicted as: " + str(mp.predict(mp.noramlize(imgPath), imgPath)))