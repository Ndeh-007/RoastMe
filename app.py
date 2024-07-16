import ctypes
import sys

from PySide6.QtWidgets import QApplication

from views.main.main_window import VMainWindow

import resources.resources_rc  # type: ignore

# os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=1"

myAppID = u'ndeh.akumah.roastMe.2.0.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppID)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = VMainWindow(app=app, args=sys.argv)
    sys.exit(app.exec())
