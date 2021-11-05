from os import sep
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib; matplotlib.use('agg')
import pandas as pd
import time

from getPulse import getPulse_cutLowFreq

# 480 x 640
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)

fig = plt.figure()
ax = fig.add_subplot(111)

heartbeat_count = 50
heartbeat_values = [0]*heartbeat_count
heartbeat_times = [time.time()]*heartbeat_count

itc = 0
while(True):
    itc += 1

    ret, frame = cap.read()

    # Our operations on the frame come here
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    x, y, w, h = 190, 270, 100, 100
    crop_img = img[y:y + h, x:x + w]

    # Display the frame in both windows
    cv2.imshow('Crop', crop_img)
    cv2.imshow('Main', img)

    # Update the list
    heartbeat_values = heartbeat_values[1:] + [np.average(crop_img)]
    heartbeat_times = heartbeat_times[1:] + [time.time()]

    ax.plot(heartbeat_times, heartbeat_values)
    fig.canvas.draw()
    plot_img_np = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    plot_img_np = plot_img_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.cla()
    
    ''' для получения отладочных данных
    if (itc == 50):
        itc = 0
        tempd = pd.DataFrame({
            "x" : heartbeat_times,
            "y" : heartbeat_values
        })
        tempd.to_csv("./pulseDataRaw/d{}.csv".format(int(time.time())), sep=",")
    '''

    if (itc == 50):
        itc = 0
        print(getPulse_cutLowFreq(heartbeat_times, heartbeat_values))

    cv2.imshow('Graph', plot_img_np)

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break

cap.release()
cv2.destroyAllWindows()