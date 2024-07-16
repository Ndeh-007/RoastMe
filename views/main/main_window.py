import sys
import traceback

import qtawesome
from PySide6.QtGui import QIcon, QPixmap, QAction
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QSystemTrayIcon, QMenu

from api.alerts import API_dispatchAlert
from api.local_storage import API_InitializeLocalStorage
from core.config_variables import APP_NAME
from utils.common_variables import LOGO_ORANGE
from utils.logger import Logger
from utils.signal_bus import signalBus
from views.floating.bubble_window import VBubbleWindow
from views.settings.settings_view import VSettingsView


class VMainWindow(QMainWindow):
    logger = Logger("application")

    def __init__(self, app: QApplication, args: list):
        super().__init__()

        self.__init_ui__()
        self.__prime__(app, args)
        self.__init_system_tray__()

        self.__connect_signals__()

    def __init_ui__(self):
        self.__bubbleView = VBubbleWindow()
        self.__settingsView = VSettingsView()

        self.setWindowIcon(QIcon(":/images/roast_me.ico"))
        self.setWindowTitle(APP_NAME)

    def __prime__(self, app: QApplication, args: list):
        self.__app = app
        self.__args = args

        # prime local storage
        API_InitializeLocalStorage()

        # signal application ready
        signalBus.initializeApplicationData.emit()

        # settings
        self.__settingsView.launch()

        # bubble
        self.__bubbleView.launch()

    def __init_system_tray__(self):
        quit_icon = qtawesome.icon("msc.chrome-close", color=LOGO_ORANGE)
        options_icon = qtawesome.icon("msc.settings-gear", color=LOGO_ORANGE)
        show_bubble_icon = qtawesome.icon("msc.eye", color=LOGO_ORANGE)
        hide_bubble_icon = qtawesome.icon("msc.eye-closed", color=LOGO_ORANGE)

        show_bubble_action = QAction(text="Show Bubble", icon=show_bubble_icon, parent=self)
        hide_bubble_action = QAction(text="Hide Bubble", icon=hide_bubble_icon, parent=self)
        settings_action = QAction(text="Settings", icon=options_icon, parent=self)
        quit_action = QAction(text="Quit", icon=quit_icon, parent=self)

        show_bubble_action.triggered.connect(self.__bubbleView.launch)
        hide_bubble_action.triggered.connect(self.__bubbleView.hide)
        settings_action.triggered.connect(self.__settingsView.launch)
        quit_action.triggered.connect(self.quitApp)

        icon = QIcon(":/images/roast_me.ico")

        self.trayMenu = QMenu()

        self.trayMenu.addAction(show_bubble_action)
        self.trayMenu.addAction(hide_bubble_action)
        self.trayMenu.addSeparator()
        self.trayMenu.addAction(settings_action)
        self.trayMenu.addSeparator()
        self.trayMenu.addAction(quit_action)

        self.trayIcon = QSystemTrayIcon()
        self.trayIcon.activated.connect(lambda: self.trayMenu.exec())
        self.trayIcon.setIcon(icon)
        self.trayIcon.setToolTip(APP_NAME)

        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.show()

    def quitApp(self):
        self.__app.quit()

    def __connect_signals__(self):
        signalBus.onTerminateApplication.connect(self.quitApp)


def exception_hook(exception: BaseException, value, tb):
    """ exception callback function """
    VMainWindow.logger.error("Unhandled exception", (exception, value, tb))
    message = '\n'.join([''.join(traceback.format_tb(tb)),
                         '{0}: {1}'.format(exception.__name__, value)])
    API_dispatchAlert(message)


sys.excepthook = exception_hook
