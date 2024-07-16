import qtawesome
from PySide6.QtCore import QPoint
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from utils.common_variables import LOGO_ORANGE
from utils.signal_bus import signalBus


class ContextMenu(QMenu):
    def __init__(self, position: QPoint):
        super().__init__()
        cls_icon = qtawesome.icon("msc.chrome-close", color=LOGO_ORANGE)
        hide_icon = qtawesome.icon("msc.eye-closed", color=LOGO_ORANGE)
        options_icon = qtawesome.icon("msc.settings-gear", color=LOGO_ORANGE)

        options_action = QAction(text="settings", icon=options_icon)
        hide_action = QAction(text="Hide", icon=hide_icon)
        quit_action = QAction(text="Quit", icon=cls_icon)

        options_action.triggered.connect(lambda: signalBus.onConfigureApplication.emit())
        quit_action.triggered.connect(lambda: signalBus.onTerminateApplication.emit())
        hide_action.triggered.connect(lambda: signalBus.onHideBubble.emit())

        # self.addAction(options_action)
        self.addAction(hide_action)
        self.addSeparator()
        self.addAction(options_action)
        self.addSeparator()
        self.addAction(quit_action)

        self.exec_(position)
