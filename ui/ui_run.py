import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from ui.ui_main import Ui


def initUi():
    app = QApplication(sys.argv)
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'sources/app_logo.png')
    app.setWindowIcon(QIcon(path))
    ex = Ui()

    sys.exit(app.exec_())