import cv2
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib; matplotlib.use('agg')
cascPath = "Cascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
#
heartbeat_count = 128
heartbeat_values = [0]*heartbeat_count
heartbeat_times = [time.time()]*heartbeat_count
fig = plt.figure()
ax = fig.add_subplot(111)
#
video_capture = cv2.VideoCapture(0)
pulse = None
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    for x, y, w, h in faces:
        cv2.rectangle(frame, (int(x + w / 2 - w / 5), int(y + h / 5 - h / 8)), (int(x + w / 2 + w / 5), int(y + h / 4)),
                      (255, 0, 0), 2)
        b = frame[x: int(x + w / 2 - w / 5), y: int(y + h / 4), :1]
        g = frame[x: int(x + w / 2 - w / 5), y: int(y + h / 4), 1:2]
        r = frame[x: int(x + w / 2 - w / 5), y: int(y + h / 4), 2:]

        # пульс как среднее значение по средним значением яркости с каждого канала
        pulse = (np.average(r) + np.average(g) + np.average(b)) / 3

        # Update data into arrays
        heartbeat_values = heartbeat_values[1:] + [pulse]
        heartbeat_times = heartbeat_times[1:] + [time.time()]

        # Update data into plot
        ax.plot(heartbeat_times, heartbeat_values)
        fig.canvas.draw()
        plot_img_np = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        plot_img_np = plot_img_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.cla()
        cv2.imshow('Graph', plot_img_np)
    cv2.putText(frame, 'Pulse: ' + str(pulse), (10, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Faces', frame)

    # Display the resulting frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
