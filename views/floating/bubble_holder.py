from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QMouseEvent, Qt, QPixmap
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QWidget

from api.content import API_fetchContent
from api.local_storage import API_fetchAppSettingsItem
from utils.signal_bus import signalBus
from views.floating.bubble import Bubble
from views.floating.floating_context_menu import ContextMenu


class BubbleHolder(QFrame):
    def __init__(self):
        super().__init__()
        self.x = 64
        self.y = 64
        self.s = QSize(self.x, self.y)
        self.resize(self.s)

        img = QLabel()
        pixmap = QPixmap(":/images/roast_me_small.png")

        img.setPixmap(pixmap)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.bubble = Bubble()
        self.bubble.hide()

        self.layout.addWidget(self.bubble)

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

        # hide the bubble after 10 seconds
        self.bubble_timer = QTimer()
        self.bubble_timer.setInterval(10000)
        self.bubble_timer.timeout.connect(self.removeInsult)
        self.bubble_timer.setSingleShot(True)

        # at every interval(ms), fetch an insult or joke
        interval = 1 * 60000  # 1 minute

        self.insult_timer = QTimer()
        self.insult_timer.setInterval(interval)
        self.insult_timer.timeout.connect(self.showInsult)
        self.insult_timer.setSingleShot(False)
        self.insult_timer.start()

        self.connectSignals()

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
        text = API_fetchContent()
        self.bubble.showBubble(text)
        signalBus.onEnlargeWindow.emit(self.bubble.sizeHint())

    def removeInsult(self):
        self.bubble.closeBubble()
        # signalBus.onReduceWindow.emit()

    def __handleSettingsUpdated(self):
        interval = API_fetchAppSettingsItem("fetch_interval")
        if interval is not None:
            self.insult_timer.setInterval(int(float(interval) * 60000))

    def connectSignals(self):
        signalBus.onSettingsUpdated.connect(self.__handleSettingsUpdated)
        signalBus.initializeApplicationData.connect(self.__handleSettingsUpdated)