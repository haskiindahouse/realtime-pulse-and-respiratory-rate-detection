import face_recognition
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib; matplotlib.use('agg')

pulse_data_len = 10
pulse_data = []
fig = plt.figure()
ax = fig.add_subplot(111)

video_capture = cv2.VideoCapture(0)

heartbeat_count = 50
heartbeat_values = [0]*heartbeat_count
heartbeat_times = [time.time()]*heartbeat_count

user_image = face_recognition.load_image_file("users/Mikhail.png")
user_face_encoding = face_recognition.face_encodings(user_image)[0]

known_face_encodings = [
    user_face_encoding,
]

face_locations = []
face_encodings = []
face_names = []

compressing_rate = 1
fcount = 0
while True:
    fcount += 1
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=1/compressing_rate, fy=1/compressing_rate)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if (fcount == 10):
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        fcount = 0

    # Display the results
    for (top, right, bottom, left) in face_locations:
        
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= compressing_rate; right *= compressing_rate; bottom *= compressing_rate; left *= compressing_rate
        
        # Coordinates for color grabber
        top1 = int(top + (bottom - top) * 0.15)
        bottom1 = int(top1 + 30)
        left1 = int(left + (right - left) / 2 - (right - left) / 20)
        right1 = int(right - (right - left) / 2 + (right - left) / 20)
        # print("{}, {}, {}, {}".format(top1, bottom1, left1, right1))

        # taking average value according to recomendations
        crop_img = cv2.cvtColor(rgb_small_frame[top1:bottom1, left1:right1], cv2.COLOR_BGR2GRAY)
        pulse1 = np.average(crop_img)
        cv2.imshow('Crop', crop_img)
        # print(crop_img)

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
        # Draw a box around forhead
        cv2.rectangle(frame, (left1, top1), (right1, bottom1), (0, 255, 0), 2)

        # display the avg color
        heartbeat_values = heartbeat_values[1:] + [pulse1]
        heartbeat_times = heartbeat_times[1:] + [time.time()]

        ax.plot(heartbeat_times, heartbeat_values)
        fig.canvas.draw()
        plot_img_np = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        plot_img_np = plot_img_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.cla()
    
        cv2.imshow('Graph', plot_img_np)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam and close window
video_capture.release()
cv2.destroyAllWindows()