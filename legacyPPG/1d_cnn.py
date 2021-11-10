from tensorflow.keras import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Считывание исходных данных
data_x = []
for i in range(10):
    rawd = pd.read_csv("data/pulse" + str(i+1) + ".csv", sep=",")
    oo = [i[0] for i in rawd.values.tolist()]
    data_x.append(oo[:700])
#print(data_x)

# Форматирование входных данных для нейросети
# Деление на обучающую и валидационную выборки, преобразование входных данных
x_train, x_test = np.array(data_x[:7]), np.array(data_x[7:])
x_train2 = pd.DataFrame(x_train)
x_test2 = pd.DataFrame(x_test)
x_train2 = np.expand_dims(x_train, axis=-1)
x_test2 = np.expand_dims(x_test, axis=-1)
print(x_train2.shape)

# Валидационные данные (сердечные сокращения за весь период графика)
data_y = [13, 12, 12, 14, 13, 12, 14, 10, 10, 12]

# Форматирование данных, с которыми нейросеть будет сравнивать результат работы
y_train, y_test = np.array(data_y[:7]), np.array(data_y[7:])
y_train2 = pd.DataFrame(y_train)
y_test2 = pd.DataFrame(y_test)
print(type(x_train))
print(type(y_train))

# Построение модели
from tensorflow import keras
from tensorflow.keras import layers, models, utils
from tensorflow.keras.layers import Conv1D, MaxPooling1D, AveragePooling1D, Dense, Dropout, Flatten

model = models.Sequential()
model.add(Conv1D(64, kernel_size=(700), input_shape=(700, 1)))
model.add(MaxPooling1D(pool_size=1))
model.add(Conv1D(64, kernel_size=(1), input_shape=(700, 1)))
model.add(AveragePooling1D(pool_size=1))

model.add(Dense(1))

opt=keras.optimizers.Adam(lr=0.000001, beta_1=0.90, beta_2=0.999)
model.compile(optimizer=opt, loss='mean_squared_error', metrics=['mean_absolute_error'])
model.summary()

# Обучение модели
history=model.fit(x_train2, y_train, validation_data=(x_test2, y_test), epochs=1000, verbose=1)