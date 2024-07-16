from PySide6 import QtCore
from PySide6.QtCore import QPoint, QSize
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout

from utils.signal_bus import signalBus
from views.floating.bubble_holder import BubbleHolder


class VBubbleWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.oldPos: QPoint | None = None
        self.newPos: QPoint | None = None
        self.smPos: QPoint | None = None
        self.wallPos: QPoint | None = None
        self.enSize: QSize | None = None
        self.xPos = 0
        self.defSize = QSize(64, 64)

        self.__init_ui__()
        self.__init_ui_attrib__()

        self.connectSignals()

    def __init_ui__(self):

        # collect the home page and attach to the main window
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.hp = BubbleHolder()
        layout.addWidget(self.hp)
        self.setLayout(layout)

        # resize the window
        screen = QApplication.screens()[0]

        x = screen.availableGeometry().topRight().x() - self.hp.x - 10
        y = screen.availableGeometry().topRight().y() + self.hp.y

        position = QPoint(x, y)
        self.oldPos = position
        self.newPos = position
        self.wallPos = position
        self.smPos = position
        self.xPos = x

        self.resize(self.defSize)

        self.move(position)

    def __init_ui_attrib__(self):
        self.setModal(False)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.oldPos is not None:
            delta = event.globalPos() - self.oldPos

            xOffset = 0
            if self.hp.bubble.isVisible():
                xOffset = self.hp.bubble.size().width()

            newPos = QPoint(self.xPos - xOffset, self.pos().y() + delta.y())
            self.newPos = newPos
            self.smPos = newPos
            self.move(newPos)
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.oldPos = None

    def enlargeWindow(self, size: QSize):
        self.enSize = size
        x = self.defSize.width() + size.width() + 20  # extra 20 to account for shift in size for new dynamic content
        y = self.defSize.height() + size.height()
        self.resize(x, y)
        self.move(self.wallPos.x() - x + 64, self.newPos.y())

    def reduceWindow(self):
        self.resize(self.defSize)
        self.move(self.wallPos.x(), self.newPos.y())

    def launch(self):
        self.show()
        self.raise_()
        self.activateWindow()
        print("bbl")

    def connectSignals(self):
        signalBus.onEnlargeWindow.connect(self.enlargeWindow)
        signalBus.onReduceBubble.connect(self.reduceWindow)
        signalBus.onHideBubble.connect(lambda : print("hidnig window"))
