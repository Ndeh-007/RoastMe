import sys

import qtawesome
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

from views.main_view import MainWindow
# import ctypes
#
# # myAppID = u'unawakened.personal.roastMe.0.0.1'
# # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppID)

# init application settings from settings file
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

icon = QIcon("./assets/roast_me.png")

tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

menu = QMenu()
quit_action = QAction("Quit", icon=qtawesome.icon("msc.close", color="#ff0000"))
quit_action.triggered.connect(app.quit)
menu.addAction(quit_action)
tray.setContextMenu(menu)

window = MainWindow()
window.show()

if __name__ == "__main__":
    app.exec()
