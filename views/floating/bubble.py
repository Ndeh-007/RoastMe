import qtawesome
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QLabel, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QFrame

from utils.signal_bus import signalBus


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

        self.copy_btn = QPushButton()
        copy_icon = qtawesome.icon("msc.copy", color="#ffffff")
        self.copy_btn.setIcon(copy_icon)
        self.copy_btn.setFlat(True)
        self.copy_btn.clicked.connect(self.copyToClipboard)

        self.close_btn.setStyleSheet("background:transparent;")
        self.copy_btn.setStyleSheet("background:transparent;")

        self.copy_feedback = QLabel("")
        self.copy_feedback.setStyleSheet(""" 
                color: #DB7231;
                font-size: 10;
                """)
        self.copy_feedback.setObjectName("CopyFeedBackLabel")
        self.copy_feedback_timer = QTimer()
        self.copy_feedback_timer.setSingleShot(True)
        self.copy_feedback_timer.setInterval(2000)
        self.copy_feedback_timer.timeout.connect(lambda: self.copy_feedback.setText(""))

        header = QWidget()
        hl = QHBoxLayout()
        hl.setContentsMargins(0, 0, 0, 0)
        hl.addWidget(self.copy_feedback)
        hl.addStretch(2)
        hl.addWidget(self.copy_btn)
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
        signalBus.onReduceBubble.emit()

    def showBubble(self, value):
        self.setText(value)
        self.show()

    def copyToClipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text.text())

        self.copy_feedback.setText("copied")
        self.copy_feedback_timer.start()
