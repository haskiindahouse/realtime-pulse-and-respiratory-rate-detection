import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft
from scipy.fftpack import fftfreq
from scipy.interpolate import interp1d
# ЛЕГКОЕ СЧИТЫВАНИЕ ПО МОЕМУ МНЕНИЮ
data = pd.read_csv('data/pulse2.csv')
data = data[[data.columns[0]]]
print(data.values)
data2 = pd.read_csv('data/pulse3.csv')
data2 = data2[[data2.columns[0]]]
# grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]
# f1 = griddata(data[['744']], data[['1']], (grid_x, grid_y), method='nearest')
data.plot()
plt.show()
# FFT
N = data.size
T = 2
x = np.linspace(0.0, N * T, N)
y = data.values
yf = fft(y)
xf = fftfreq(data.size, d=T)
plt.plot(x[:x.size//2], abs(yf)[:yf.size//2])
plt.show()
# INTERPOLATE
x1 = sorted([1., 0.88, 0.67, 0.50, 0.35, 0.27, 0.18, 0.11, 0.08, 0.04, 0.04, 0.02])
y1 = [0., 13.99, 27.99, 41.98, 55.98, 69.97, 83.97, 97.97, 111.96, 125.96, 139.95, 153.95]
x1 = np.asarray(x1)
y1 = np.asarray(y1).squeeze()
new_length = 25
# new_x = np.linspace(x.min(), x.max(), new_length)
# new_y = interp1d(x, y, kind='cubic')(new_x)
# plt.plot(new_x, new_y)
# plt.show()
