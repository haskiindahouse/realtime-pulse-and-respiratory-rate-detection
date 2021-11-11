from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, QSize, QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QImage, QPixmap, QIcon

from database import createDB
from ui.stylesheets import plainTextStyle, pushButtonStyle, mainWindowStyle, lineEditStyle
from model.thread import Thread


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

        self.customLog = QPlainTextEdit(self)
        self.customLog.setStyleSheet(plainTextStyle())

        self.customLog.setReadOnly(True)
        self.customLog.blockCountChanged.connect(self.logAutoClear)

        self.con = createDB.createConnection(self.customLog)
        createDB.createTable(self.con, self.customLog)

        self.cameraRoll = QLabel(self)
        self.th = Thread(self.con, self.customLog)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

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
        Конвертирует из QPixmap into bytes.
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