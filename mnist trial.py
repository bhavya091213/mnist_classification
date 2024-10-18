import keras
from keras import layers
import matplotlib.pyplot as mpl
import numpy as np
import sklearn.metrics

#loading dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data(path="mnist.npz")


#`sc`aling
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
    keras.layers.Dense(100, activation="relu"),
    keras.layers.Dense(50, activation="relu"),
    keras.layers.Dense(10, activation='sigmoid')
])





model.compile(
    optimizer= 'Adamax',
    loss= 'sparse_categorical_crossentropy',
    metrics=[
        'accuracy', # regular accuracy
        #'mae' # mean absolute error
        
    ]
)

#fitting
print('STARTING FITTING')
model.fit(x_train_flat, y_train, epochs = 32)


#evaluation of metrics

# Scikit learn is used to measure precision, recall, and f1-score
y_pred = model.predict(x_test_flat)
y_pred_bool = np.argmax(y_pred, axis = 1)
print(sklearn.metrics.classification_report(y_test, y_pred_bool))
# model.evaluate(x_test_flat, y_test) # EVALUATE IS ONLY FOR THINGS LIKE FIGURING OUT METTRICS
# technically model.evaluate is redundant because sklearn already does it for you within classification_report



model.save('./models/mod1.keras')