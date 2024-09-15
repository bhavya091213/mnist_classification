import keras
from keras import models

model = models.load_model('my_model.keras')
print("loaded model")


