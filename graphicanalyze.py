import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def lEMax(dt, startValue, endValue):
    lMax = dt[startValue]
    index = startValue
    for i in range(startValue, endValue):
        if dt[i] > lMax:
            index = i
            lMax = dt[i]
    return index


def lEMin(dt, startValue, endValue):
    lMin = dt[startValue]
    index = startValue
    for i in range(startValue, endValue):
        if dt[i] < lMin:
            index = i
            lMin = dt[i]
    return index


def localExtremuses(dt, controlValueMAX, controlValueMIN):
    startValue = 0
    endValue = 50
    resultMAX = []
    resultMIN = []
    while endValue < len(dt):
        indexMAX = int(lEMax(dt, startValue, endValue))
        indexMIN = int(lEMin(dt, startValue, endValue))
        currentMIN = dt[indexMIN]
        currentMAX = dt[indexMAX]
        if currentMAX > controlValueMAX:
            resultMAX.append(indexMAX)
        if currentMIN < controlValueMIN:
            resultMIN.append(indexMIN)
        startValue = endValue
        endValue += 20
    return list(set(resultMAX)), list(set(resultMIN))


def forplotting(data, controlValueMAX, controlValueMIN):
    s = pd.Series(data.values.ravel())
    min_indexes, max_indexes = localExtremuses(s, controlValueMAX, controlValueMIN)
    min_values = []
    max_values = []
    array = data.values.ravel()
    for index in min_indexes:
        min_values.append(array[index])
    for index in max_indexes:
        max_values.append(array[index])
    return [min_indexes, min_values], [max_indexes, max_values]


# ЛЕГКОЕ СЧИТЫВАНИЕ ПО МОЕМУ МНЕНИЮ
# list_of_files = os.listdir("data")
# for file in list_of_files:
#    data = pd.read_csv("data/" + file)
#    data[[data.columns[0]]].plot()
#    plt.title(file)
#   plt.show()
#   fxMIN, fxMAX = forplotting(data, 510, 500)
#    print(file + " " + str(len(fxMAX[0])))
data = pd.read_csv('data/pulse1.csv')
data = data[[data.columns[0]]]
# GRIDDATA
# grid_x, grid_y = np.mgrid[0:3000:3000j, 0:3000:3000j]
# grid_z0 = griddata(data[data.columns[0]].values, data[data.columns[1]].values, grid_x, method='nearest')
# plt.plot(grid_z0)
# plt.show()
data.plot()
plt.title('Исходный график')
plt.show()
# FFT
'''
N = data.size
T = 2
x = np.linspace(0.0, N * T, N)
y = data.values
yf = fft(y)
xf = fftfreq(data.size, d=T)
xK = xf[:xf.size//2]
yK = abs(yf)[:yf.size//2]
plt.plot(xK, yK)
yf = fft(yf)
yK = abs(yf)[:yf.size//2]
plt.plot(xK, yK)
plt.show()
'''
# Поиск всех экстремумов ДЛЯ ПЕРВОГО
fxMIN, fxMAX = forplotting(data, 500, 480)
# График по экстремумам
length = len(fxMIN[1]) if len(fxMIN[1]) <= len(fxMAX[1]) and len(fxMIN[1]) != 0 else len(fxMAX[1])
i = 0
nData = []
while i < length:
    nData.append(fxMIN[1][i])
    nData.append(fxMAX[1][i])
    i += 1
plt.plot(nData)
plt.title('График по найденным экстремумам')
plt.show()
# INTERPOLATE
mylist = data.values.ravel().tolist()
for i in range(len(mylist)):
    if mylist[i] not in nData:
        mylist[i] = np.nan
s = pd.Series(mylist).interpolate(method='akima')
plt.plot(s)
plt.title('akima-interpolation')
plt.show()
