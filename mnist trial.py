import keras
from keras import layers
import matplotlib.pyplot as mpl
import numpy as np


#loading dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data(path="mnist.npz")


#scaling
x_train = x_train/255
x_test = x_test/255

#reshape from 2d array to 1d array
x_train_flat = x_train.reshape(len(x_train), 28*28)
x_test_flat = x_test.reshape(len(x_test), 28*28)

#print statements
'''print(x_train_flat.shape)
print(x_test_flat.shape)'''


#model declaration
model = keras.Sequential([
    keras.layers.Dense(100, activation="relu"),
    keras.layers.Dense(10, activation='sigmoid')
])



    

model.compile(
    optimizer= 'adam',
    loss= 'sparse_categorical_crossentropy',
    metrics=['accuracy']
)

#fitting
print('STARTING FITTING')
model.fit(x_train_flat, y_train, epochs = 10)


#evalutation

model.evaluate(x_test_flat, y_test)

model.save('my_model.keras')