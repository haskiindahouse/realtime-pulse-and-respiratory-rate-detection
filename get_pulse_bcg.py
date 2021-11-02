import face_recognition
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib; matplotlib.use('agg')
import pandas as pd
import time

from getPulse import getPulse_cutLowFreq

# 480 x 640 avg 29-30 fps
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)

fig = plt.figure()
ax = fig.add_subplot(111)

heartbeat_count = 250
heartbeat_values = [0]*heartbeat_count
heartbeat_times = [time.time()]*heartbeat_count

start_time = time.time()
count_frames = 0

compressing_rate = 4

# saving these values for next iterations
gx, gy, gw, gh = 100, 100, 100, 100
while(True):
    count_frames += 1

    ret, frame = cap.read()

    small_frame = cv2.resize(frame, (0, 0), fx=1/compressing_rate, fy=1/compressing_rate)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = []
    # Only process every other frame of video to save time
    if (count_frames % 10 == 0):
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        print(face_locations)

    for (top, right, bottom, left) in face_locations:
        
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= compressing_rate; right *= compressing_rate; bottom *= compressing_rate; left *= compressing_rate
        
        # Coordinates for color grabber
        gx = ((right - left) / 2) + left - (right - left) / 4
        gy = bottom - ((bottom - top) / 5)

        gh = (bottom - top) / 2
        gw = (right - left) / 2

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Our operations on the frame come here
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    crop_img = img[int(gy - gh):int(gy), int(gx):int(gx + gw)]

    heartbeat_values = heartbeat_values[1:] + [np.average(crop_img)]
    heartbeat_times = heartbeat_times[1:] + [time.time()]

    if (count_frames % 250 == 0):
        itc = 0
        tempd = pd.DataFrame({
            "x" : heartbeat_times,
            "y" : heartbeat_values
        })
        tempd.to_csv("./pulseDataRaw/d{}.csv".format(int(time.time())), sep=",")
   

    # Display the frame in both windows
    cv2.imshow('Crop', crop_img)
    cv2.imshow('Main', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):

        end_time = time.time()
        print(count_frames / (end_time - start_time))

        break

cap.release()
cv2.destroyAllWindows()