from tensorflow import keras
from tensorflow.keras import layers, models, utils, activations
from tensorflow.keras.layers import Conv1D, Conv2D, BatchNormalization, Dense, MaxPooling2D, MaxPooling1D, Dropout, Flatten, Activation, LSTM
from tensorflow.keras import optimizers
from tensorflow.keras import preprocessing
import numpy as np
import pandas as pd

def legacy_predict(model1):
    data_x = []
    for i in range(10):
        rawd = pd.read_csv("data/pulse" + str(i+1) + ".csv", sep=",")
        oo = [i[0] for i in rawd.values.tolist()]
        data_x.append(oo[:700])

    data_n = np.array(data_x)
    data = np.expand_dims(data_n, axis=2)

    print(model1.predict(data))

def get_prediction_700():
    model = keras.models.load_model('data/1dcnn')
    return model.predict()

# Импорт заранее созданной и обученной модели
if __name__ == "__main__":
    model = keras.models.load_model('data/1dcnn')
    model.summary()

    legacy_predict(model)