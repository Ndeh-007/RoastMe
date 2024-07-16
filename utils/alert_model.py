from typing import Literal

from PySide6.QtGui import Qt


class AlertDataModel:
    def __init__(self, msg: str, mode: Literal["error", "warning", "event"] = "error"):
        self.__msg = msg
        self.__mode = mode

        self.__color = Qt.GlobalColor.red

        self.__config()

    def __config(self):
        if self.__mode == "error":
            self.__color = Qt.GlobalColor.red
        if self.__mode == "warning":
            self.__color = Qt.GlobalColor.yellow
        if self.__mode == "event":
            self.__color = Qt.GlobalColor.green

    def setMode(self, mode):
        self.__mode = mode
        self.__config()

    def setText(self, text):
        self.__msg = text

    def text(self):
        return self.__msg

    def mode(self):
        return self.__mode

    def color(self):
        return self.__color
