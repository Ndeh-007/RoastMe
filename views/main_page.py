import python_avatars as pa
import qtawesome
from PySide6.QtCore import QPoint, QSize, QTimer
from PySide6.QtGui import QAction, QMouseEvent, Qt, QPixmap
from PySide6.QtWidgets import QFrame, QMenu, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, \
    QWidget

from core.api import fetchInsult, fetchJoke
from core.context_menu import open_settings, quit_application
from core.signalBus import signalBus


class MainPage(QFrame):
    def __init__(self):
        super().__init__()
        self.x = 64
        self.y = 64
        self.s = QSize(self.x, self.y)
        self.resize(self.s)
        self.toggler = False

        img = QLabel()
        pixmap = QPixmap("./assets/roast_me_small.png")

        img.setPixmap(pixmap)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.bubble = Bubble()
        self.bubble.hide()

        self.layout.addWidget(self.bubble)

        # self.layout.addWidget(img)

        i = QWidget()
        il = QVBoxLayout()
        il.setContentsMargins(0, 0, 0, 0)
        il.addWidget(img)
        il.addStretch()
        i.setLayout(il)
        self.layout.addWidget(i)
        self.setLayout(self.layout)
        self.setObjectName("content")
        self.setStyleSheet("""
            QFrame#content{
                background:transparent;
            }
        """)

        # hide the bubble after 5seconds
        self.bubble_timer = QTimer()
        self.bubble_timer.setInterval(10000)
        self.bubble_timer.timeout.connect(self.removeInsult)
        self.bubble_timer.setSingleShot(True)

        # at every interval(ms), fetch an insult
        interval = 1800000

        self.insult_timer = QTimer()
        self.insult_timer.setInterval(interval)
        self.insult_timer.timeout.connect(self.showInsult)
        self.insult_timer.setSingleShot(False)
        self.insult_timer.start()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.RightButton:
            pos = event.globalPos()
            ContextMenu(pos)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        super().mouseDoubleClickEvent(event)
        self.showInsult()
        self.insult_timer.start()

    def showInsult(self):
        if self.toggler:
            text = fetchInsult()
        else:
            text = fetchJoke()
        self.bubble.showBubble(text)
        self.bubble_timer.start()
        signalBus.onEnlargeWindow.emit(self.bubble.sizeHint())
        self.toggler = not self.toggler

    def removeInsult(self):
        self.bubble.closeBubble()
        signalBus.onReduceWindow.emit()


class Avatar:
    def __init__(self):
        self.avatar: Avatar | None = None
        self.load_avatar()

    def load_avatar(self):
        self.avatar = pa.Avatar.random()
        self.avatar.render("./assets/avatar.png")


class ContextMenu(QMenu):
    def __init__(self, position: QPoint):
        super().__init__()
        options_action = QAction(text="Options")
        cls_icon = qtawesome.icon("msc.chrome-close", color="#ff0000")
        quit_action = QAction(text="Quit", icon=cls_icon)

        options_action.triggered.connect(open_settings)
        quit_action.triggered.connect(quit_application)

        # self.addAction(options_action)
        self.addAction(quit_action)

        self.exec_(position)


class Bubble(QFrame):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 5, 5, 5)

        self.close_btn = QPushButton()
        cls_icon = qtawesome.icon("msc.close", color="#db7231")
        self.close_btn.setIcon(cls_icon)
        self.close_btn.setFlat(True)
        self.close_btn.clicked.connect(self.closeBubble)

        self.close_btn.setStyleSheet("background:transparent;")

        header = QWidget()
        hl = QVBoxLayout()
        hl.setAlignment(Qt.AlignmentFlag.AlignRight)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.addWidget(self.close_btn)
        header.setLayout(hl)

        layout.addWidget(header)

        self.text = QLabel()
        self.text.setWordWrap(True)
        layout.addWidget(self.text)

        self.text.setStyleSheet("""
            color:white;
            font-size: 13px;
            font-weight:600;
        """)
        self.setLayout(layout)

        self.setObjectName("bubble")
        self.setStyleSheet("""
            QFrame#bubble{
                background: black;
            }
        """)

        layout.addStretch()

    def setText(self, message):
        self.text.setText(message)

    def closeBubble(self):
        self.hide()

    def showBubble(self, value):
        self.setText(value)
        self.show()
