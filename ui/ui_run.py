import sys

import cv2
from PyQt5.QtWidgets import *

from ui_main import Ui


def initUi():
    app = QApplication(sys.argv)

    ex = Ui()

    sys.exit(app.exec_())


if __name__ == '__main__':
   initUi()