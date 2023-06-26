from PySide6 import QtCore
from PySide6.QtCore import QPoint, QSize
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QApplication, QMainWindow

from core.signalBus import signalBus
from views.main_page import MainPage


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.oldPos: QPoint | None = None
        self.newPos: QPoint | None = None
        self.smPos: QPoint | None = None
        self.enSize: QSize | None = None
        self.xPos = 0
        self.defSize = QSize(64, 64)
        self.__init_UI__()

    def __init_UI__(self):
        self.setWindowIcon(QIcon("./assets/roast_me.png"))

        # collect the home page and attach to the main window
        hp = MainPage()
        self.setCentralWidget(hp)

        # resize the window
        screen = QApplication.screens()[0]

        x = screen.availableGeometry().topRight().x() - hp.x - 10
        y = screen.availableGeometry().topRight().y() + hp.y

        position = QPoint(x, y)
        self.oldPos = position
        self.newPos = position
        self.smPos = position
        self.xPos = x
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.resize(self.defSize)

        self.move(position)
        self.setContentsMargins(0, 0, 0, 0)

        # modify drop shadow effect. this does not work check it.

        self.connectSignals()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.oldPos is not None:
            delta = event.globalPos() - self.oldPos
            newPos = QPoint(self.xPos, self.pos().y() + delta.y())
            self.newPos = newPos
            self.smPos = newPos
            self.move(newPos)
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.oldPos = None

    def enlargeWindow(self, size: QSize):
        self.enSize = size
        x = self.defSize.width() + size.width()
        y = self.defSize.height() + size.height()
        self.resize(x, y)
        self.move(self.newPos.x() - x + 64, self.newPos.y())

    def reduceWindow(self):
        s = self.size()
        x = s.width() - 64
        y = s.height() - 64

        self.resize(64, 64)

        self.move(self.xPos, y)

    def quiteApp(self):
        self.close()

    def connectSignals(self):
        signalBus.onCloseWindow.connect(self.quiteApp)
        signalBus.onEnlargeWindow.connect(self.enlargeWindow)
        signalBus.onReduceWindow.connect(self.reduceWindow)
