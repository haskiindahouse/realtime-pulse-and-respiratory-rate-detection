from datetime import time
import os
import pandas as pd
import matplotlib.pyplot as plt
import heartpy as hp
from scipy.signal import find_peaks
import numpy

def normalizeData(data : list):
    maxv = max(data)
    minv = min(data)

    res = []
    for i in data:
        res.append((i - minv)/(maxv - minv))

    return res

if __name__ == "__main__":
    files = os.listdir(path="./pulseDataRaw")

    for filename in files:
        rawData = pd.read_csv("./pulseDataRaw/{}".format(filename), sep=",")
    
        timeData = rawData['x'].to_list()
        pulseData = rawData['y'].to_list()

        elapsedTime = timeData[-1] - timeData[0]
        print(elapsedTime)

        curr_hz = len(pulseData)/elapsedTime

        pulseData2 = normalizeData(pulseData)
        # print(pulseData2)

        peaks, _ = find_peaks(pulseData, distance=4)

        # plt.plot(peaks, pulseData2[peaks], "x")
        # не знаю почему, но штука выше не работает, хотя в документации описана

        plt.plot(pulseData)
        print("Pulse is:", len(peaks)*(60/curr_hz))

        for i in range(len(peaks)):
            plt.plot(peaks[i], pulseData[peaks[i]], "x")
        plt.show()