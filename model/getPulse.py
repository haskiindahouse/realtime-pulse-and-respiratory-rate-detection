from datetime import time
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, butter, lfilter, filtfilt
import numpy


def normalizeData(data : list):
    maxv = max(data)
    minv = min(data)

    res = []
    for i in data:
        res.append((i - minv)/(maxv - minv))

    return res


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a


def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y


def PCA_exp():
    pass


def getPulse_simplePeaks(timeData: list, pulseData: list):
    # Сколько секунд между началом и концом записи
    elapsedTime = timeData[-1] - timeData[0]

    # Частота записи, сколько значений в секунду - Герцы
    curr_hz = len(pulseData)/elapsedTime

    # Нормализация
    pulseDataТ = normalizeData(pulseData)

    # Подсчёт количества пиков на графике
    peaks, _ = find_peaks(pulseDataТ, distance=4)
    
    pulse = len(peaks)*(60/curr_hz)
    return pulse


def getPulse_cutLowFreq(timeData: list, pulseData: list):
    normalizeData(pulseData)

    # using two unix times from start and end
    elapsedTime = timeData[-1] - timeData[0]
    
    # sample rate
    fs = len(pulseData)/elapsedTime

    # frequency which we should throw out using filtering
    lowcut = (fs / 3) - 1

    # cutting off low probability results
    max_bpm = 170
    max_bpm_per_sec = max_bpm / fs
    max_beats_spreading_in_one_sec = int(fs / max_bpm_per_sec) - 1

    filteredPulseData = butter_highpass_filter(pulseData, lowcut, fs, order=4)
    # основная настройка гиперпараметров здесь
    peaks, _ = find_peaks(filteredPulseData, distance=max_beats_spreading_in_one_sec)
    return int(len(peaks) * (60 / fs))


def getPulse_cutLowFreq_ex():
    files = os.listdir(path="./pulseDataRaw")
    ret = 0
    print("len files = " + str(len(files)))

    for filename in files:

        rawData = pd.read_csv("./pulseDataRaw/{}".format(filename), sep=",")
    
        timeData = rawData['x'].to_list()
        pulseData = rawData['y'].to_list()

        pulseDataN = normalizeData(pulseData)

        # using two unix times from start and end
        elapsedTime = timeData[-1] - timeData[0]
    
        # sample rate
        fs = len(pulseData)/elapsedTime

        # frequency which we should throw out using filtering
        lowcut = (fs / 3) - 1

        #plt.figure(1)
        #plt.clf()

        # cutting off low probability results
        max_bpm = 170
        max_bpm_per_sec = max_bpm / fs
        max_beats_spreading_in_one_sec = int(fs / max_bpm_per_sec) - 1

        #plt.plot(timeData, pulseDataN, label='Noisy signal')

        filteredPulseData = butter_highpass_filter(pulseData, lowcut, fs, order=4)

        #plt.plot(timeData, filteredPulseData, label='Filtered signal')

        # основная настройка гиперпараметров здесь
        peaks, _ = find_peaks(filteredPulseData, distance=max_beats_spreading_in_one_sec)
        print("Pulse is:", int(len(peaks)*(60/fs)))
        ret += len(peaks) * 60 / fs
        #for i in range(len(peaks)):
        #    plt.plot(timeData[peaks[i]], filteredPulseData[peaks[i]], "x")

        #plt.grid(True)
        #plt.axis('tight')
        #plt.legend(loc='upper left')

        # Показывать вспомогательные plot - для наглядности вычислений
        #plt.show()
    if not ret:
        return None
    return ret / len(files)


def getPulse_enchanced_ex2():
    # Провал: для такого фильтра нужна большая частота считывания сигнала
    files = os.listdir(path="../pulseDataRaw")

    for filename in files:

        rawData = pd.read_csv("./pulseDataRaw/{}".format(filename), sep=",")
    
        timeData = rawData['x'].to_list()
        pulseData = rawData['y'].to_list()
        
        # using two unix times from start and end
        elapsedTime = timeData[-1] - timeData[0]
    
        # sample rate
        #fs = len(pulseData)/elapsedTime
    
        fs = 20

        # frequencies which we should throw out using filtering
        lowcut = 5
        highcut = 7

        plt.figure(1)
        plt.clf()

        plt.plot(timeData, pulseData, label='Noisy signal')

        filteredPulseData = butter_bandpass_filter(pulseData, lowcut, highcut, fs, order=6)

        plt.plot(timeData, filteredPulseData, label='Filtered signal')
        plt.grid(True)
        plt.axis('tight')
        plt.legend(loc='upper left')

        plt.show()


def getPulse_enchanced_ex():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import freqz

    # Sample rate and desired cutoff frequencies (in Hz).
    fs = 5000.0
    lowcut = 500.0
    highcut = 1250.0

    # Plot the frequency response for a few different orders.
    plt.figure(1)
    plt.clf()
    for order in [3, 6, 9]:
        b, a = butter_bandpass(lowcut, highcut, fs, order=order)
        w, h = freqz(b, a, worN=2000)
        plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)

    plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],
             '--', label='sqrt(0.5)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid(True)
    plt.legend(loc='best')

    # Filter a noisy signal.
    T = 0.05
    nsamples = T * fs
    t = np.linspace(0, T, int(nsamples), endpoint=False)
    a = 0.02
    f0 = 600.0
    x = 0.1 * np.sin(2 * np.pi * 1.2 * np.sqrt(t))
    x += 0.01 * np.cos(2 * np.pi * 312 * t + 0.1)
    x += a * np.cos(2 * np.pi * f0 * t + .11)
    x += 0.03 * np.cos(2 * np.pi * 2000 * t)
    plt.figure(2)
    plt.clf()
    plt.plot(t, x, label='Noisy signal')

    y = butter_bandpass_filter(x, lowcut, highcut, fs, order=6)
    plt.plot(t, y, label='Filtered signal (%g Hz)' % f0)
    plt.xlabel('time (seconds)')
    plt.hlines([-a, a], 0, T, linestyles='--')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper left')

    plt.show()


def exampleFunc():
    # example method which working with data from ./pulseDataRaw directory
    # there are located the most quality data collected using PPG or BCG
    # method using web camera
    files = os.listdir(path="../pulseDataRaw")

    for filename in files:

        rawData = pd.read_csv("./pulseDataRaw/{}".format(filename), sep=",")
    
        timeData = rawData['x'].to_list()
        pulseData = rawData['y'].to_list()

        print("Pulse2 is:", getPulse_simplePeaks(timeData, pulseData))

        elapsedTime = timeData[-1] - timeData[0]
        print(elapsedTime)

        curr_hz = len(pulseData)/elapsedTime

        pulseData2 = normalizeData(pulseData)
        # print(pulseData2)

        peaks, _ = find_peaks(pulseData, distance=4)
        print("Pulse is:", len(peaks)*(60/curr_hz))
        plt.plot(pulseData)
        
        # plt.plot(peaks, pulseData2[peaks], "x")
        # не знаю почему, но штука выше не работает, хотя в документации описана
        # Я её заменил просто циклом по peaks, расположенным ниже

        for i in range(len(peaks)):
            plt.plot(peaks[i], pulseData[peaks[i]], "x")
        plt.show()


def getPulse(heartBeatTimes, heartBeatValues):
    return getPulse_cutLowFreq(heartBeatTimes, heartBeatValues)



'''
    в качестве данных по каждому графику мы получаем данные по двум осям:
    1 - условные единицы, представляющие значения сложной величины, по изменению
    которой мы определяем частоту пульса человека
    2 - время, в которое было зафиксировано одно соответствующее по индексу
    значение, в формате unix-time (или количество секунд от 1.1.1970)
        
    В .csv файлах три колонки: индекс | время | значение случайной величины
        
    Небольшая техническая ремарка: величина названа СЛОЖНОЙ, потому-что представляет
    собой значение, полученное на основе цветовых характеристик изображения с применением
    различных методов. Мы можем использовать как получение среднего цвета какой-то части 
    изображения в ЧБ тонах, так и значение только лишь зелёного канала, что, согласно 
    некоторым источникам, более предпочтительно для PPG метода
        
    Что касается не PPG (фотоплетизмографии), а BCG (баллистокардиографии)
    Эта задача более сложная, но, согласно некоторым исследования и статьям
    имеет более большую точность, но располагает большим количеством методов
    для фильтрации значимых данных:
    1. Нужно выполнить задачу трекинга некоторых частей лица человека, и 
    отслеживать перемещения вверх-вниз, по вертикальным координатам
    (Обусловлено это тем, что голову от дыхания и от сердцебиения слегка шатает,
    преимущественно в вертикальном направлении, эксперименты показывают, что именно
    при считывании движений вверх-вниз шумов меньше всего, вне зависимости от гиперпараметров)
    2. Нужно отфильтровать полученные изменения данных с течением времени по частотным
    характеристикам. В рамках статьи берутся значения от 20 до 200 герц, так как пульс
    лежит примерно в этом диапазоне. Досадно, что и дыхание, от влияния на результат
    которого мы стремимся уйти, остаётся в той или иной мере после фильтрации в выбранном
    диапазоне.
    3. Применение PCA (Метод основных компонент, Principal component analisys).
    Обычно он применяется в рамках уменьшения количества входных данных с помощью уничтожения
    самого незначещего измерения данных. Здесь мы с его помощью получаем самые значащие
    вектора данных и выявляем среди них ту, что содержит в себе большую часть данных об
    перемещении головы из-за сердечных сокращений.
    4. Далее, мы просто применяем алгоритм подсчёта пиков графика, параметры которого являются
    гиперпараметрами, подбор которых производится в рамках возможных значений пульса.
'''