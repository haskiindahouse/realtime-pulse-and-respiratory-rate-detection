import os
import cv2
import face_recognition
import numpy as np
import sys
from database import createDB
from stylesheets import plainTextStyle, pushButtonStyle, mainWindowStyle, lineEditStyle

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot, QSize, QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QImage, QPixmap, QIcon


class Ui(QWidget):

    def __init__(self):
        super().__init__()
        self.initUi()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.cameraRoll.setPixmap(QPixmap.fromImage(image))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.exit()

    def exit(self):
        self.th.destroy()



    def initUi(self):
        vBoxLayout = QVBoxLayout(self)
        self.userName = QLineEdit(self)
        self.userName.setStyleSheet(lineEditStyle())
        self.addUserBtn = QPushButton(self)
        self.addUserBtn.setStyleSheet(pushButtonStyle())
        self.addUserBtn.setFixedSize(50, 50)
        addUserLogo = QPixmap('sources/add_user_logo.png')
        addUserIcon = QIcon(addUserLogo)
        self.addUserBtn.setIcon(addUserIcon)
        self.addUserBtn.setIconSize(QSize(50, 50))
        self.addUserBtn.clicked.connect(self.appendUser)

        self.cameraRoll = QLabel(self)
        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

        self.customLog = QPlainTextEdit(self)
        self.customLog.setStyleSheet(plainTextStyle())

        self.customLog.setReadOnly(True)
        self.customLog.blockCountChanged.connect(self.logAutoClear)

        self.con = createDB.createConnection(self.customLog)
        createDB.createTable(self.con, self.customLog)
        hBoxLayout = QHBoxLayout(self)
        hBoxLayout.addWidget(self.cameraRoll)
        hBoxLayout.addWidget(self.userName)
        hBoxLayout.addWidget(self.addUserBtn)

        vBoxLayout.addLayout(hBoxLayout)
        vBoxLayout.addWidget(self.customLog)
        self.setLayout(vBoxLayout)
        self.move(300, 300)
        self.setWindowIcon(QIcon('sources/app_logo.png'))
        self.setStyleSheet(mainWindowStyle())
        self.setWindowTitle('PULSER 1.0')
        self.resize(800, 500)
        self.show()

    def appendUser(self):
        """
        Добавляет пользователя в бд для дальнейшего отслеживания его параметров.
        """
        userName = self.userName.text()
        # TODO
        # AveragePulse сейчас - просто я значение ввел
        averagePulse = 60
        createDB.insertBLOB(self.con, userName, averagePulse, self.pixmapToBytes())
        self.printLog("User " + userName + " was added!")

    def pixmapToBytes(self):
        """
        Конвертирует из QPixmap into bytes
        """
        ba = QByteArray()
        buff = QBuffer(ba)
        buff.open(QIODevice.WriteOnly)
        ok = self.cameraRoll.pixmap().save(buff, "PNG")
        assert ok
        pixmap_bytes = ba.data()
        self.printLog("Converting to bytes successful!")
        return pixmap_bytes

    def printLog(self, string):
        """
        Печатает string into your log.
        :return:
        """
        self.customLog.appendPlainText(str(string))

    def bytesToPixmap(self, pixmapBytes):
        """
        Конвертирует из bytes into QPixmap
        """
        ba = QByteArray(pixmapBytes)
        pixmap = QPixmap()
        ok = pixmap.loadFromData(ba, "PNG")
        assert ok
        self.printLog("Converting to QPixmap successful!")

    def logAutoClear(self):
        """
        Очищает QPlainText каждые 10 записей
        """
        blockCount = self.customLog.blockCount()
        if blockCount > 10:
            self.customLog.clear()


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        # TODO
        # Добавить кнопку возможность выбора католога с пользователями
        # Придумать как хранить их лучше (папка с .png?)
        faceRec = FaceRecognition('/Users/mihailmurunov/PycharmProjects/realtime-pulse-and-respiratory-rate-detection/users')
        while True:
            ret, frame = self.cap.read()
            faceRec.initFaceRecognition(frame)
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    def destroy(self):
        # TODO
        # Какая-то ошибка из-за неправильного завершения приложения
        self.cap.release()
        cv2.destroyAllWindows()


class FaceRecognition:
    def __init__(self, filePath):
        super().__init__()
        self.known_face_encodings = []
        self.known_face_names = []
        self.process_this_frame = True
        self.face_locations = []
        self.face_names = []
        self.setUpUsers(filePath)

    def setUpUsers(self, filePath):
        """
        Задает список пользователей по выбору папки.
        """
        filelist = [file for file in os.listdir(filePath) if file.endswith('.png')]
        for fileName in filelist:
            user_image = face_recognition.load_image_file(filePath + '/' + fileName)
            user_face_encoding = face_recognition.face_encodings(user_image)[0]
            self.known_face_encodings.append(user_face_encoding)
            self.known_face_names.append(fileName)

    def resize(self, frame):
        """
        Изменение формата для более быстрого определения лиц на камере
        """
        self.small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    def bgrToRgb(self):
        self.rgb_small_frame = self.small_frame[:, :, ::-1]

    def findFace(self):
        self.face_locations = face_recognition.face_locations(self.rgb_small_frame)
        face_encodings = face_recognition.face_encodings(self.rgb_small_frame, self.face_locations)
        self.face_names = []
        for face in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face)
            name = "Unknown"
            face_distances = face_recognition.face_distance(self.known_face_encodings, face)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            self.face_names.append(name)

    def initFaceRecognition(self, frame):
        self.resize(frame)
        self.bgrToRgb()
        if self.process_this_frame:
            self.findFace()
        self.process_this_frame = not self.process_this_frame
        self.displayResults(frame)

    def displayResults(self, frame):
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            top_fhead = top
            bottom_fhead = int(top + (bottom - top) / 50)
            left_fhead = int(left + (right - left) / 2 - (right - left) / 50)
            right_fhead = int(right - (right - left) / 2 + (right - left) / 50)
            pulse = np.average(self.rgb_small_frame)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left_fhead, top_fhead), (right_fhead, bottom_fhead), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.rectangle(frame, (left - 1, bottom), (right + 1, bottom + 36), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            cv2.putText(frame, str(pulse), (left + 6, bottom + 35), font, 1.0, (255, 255, 255), 1)
