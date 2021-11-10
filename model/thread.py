from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage
import cv2
from model.faceRecognition import FaceRecognition


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, con, customLog):
        super().__init__()
        self.con = con
        self.customLog = customLog

    def run(self):
        self.cap = cv2.VideoCapture(0)
        # TODO
        # Добавить кнопку возможность выбора католога с пользователями
        # Придумать как хранить их лучше (папка с .png?)
        faceRec = FaceRecognition(self.con, self.customLog)
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