from PySide6.QtGui import Qt, QTextCursor, QTextCharFormat
from PySide6.QtWidgets import QTextEdit

from utils.alert_model import AlertDataModel
from utils.signal_bus import signalBus


class VConsole(QTextEdit):
    def __init__(self):
        super().__init__()

        signalBus.writeToConsole.connect(self.__handleWriteToOutput)

    def __handleWriteToOutput(self, data: object):
        if isinstance(data, str):
            self.appendToViewer(data)

        if isinstance(data, AlertDataModel):
            self.appendToViewer(data.text(), data.color())

    def appendToViewer(self, data: str, color=Qt.GlobalColor.lightGray):
        """
        handles writing data to the preview section of the item
        By default, the viewer(QTextEdit) takes in string values. current, it appends the string
        values to the viewer.

        this function can be overridden
        depending on the kind of previewer has been set
        @param data:
        @param color:
        @return:
        """
        self.moveCursor(QTextCursor.MoveOperation.End)

        cursor = self.textCursor()

        charFormat = QTextCharFormat()
        charFormat.setForeground(color)

        cursor.setCharFormat(charFormat)
        cursor.insertText("\n")
        cursor.insertText(data)

        sb = self.verticalScrollBar()
        sb.setValue(sb.maximum())
