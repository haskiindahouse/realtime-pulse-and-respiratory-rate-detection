import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft
# ЛЕГКОЕ СЧИТЫВАНИЕ ПО МОЕМУ МНЕНИЮ
data = pd.read_csv('data/pulse2.csv')
data = data[[data.columns[0]]]
data2 = pd.read_csv('data/pulse3.csv')
data2 = data2[[data2.columns[0]]]
# grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]
# f1 = griddata(data[['744']], data[['1']], (grid_x, grid_y), method='nearest')
plt.show()