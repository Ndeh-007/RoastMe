from time import sleep
import pywhatkit as pyw

from PySide6.QtCore import QObject, Signal


class Worker(QObject):
    atInterval = Signal()

    def __init__(self, interval):
        super().__init__()
        self.counter(interval)

    def counter(self, interval):
        count = 0
        while count < interval:
            sleep(1)
            count += 1
        self.atInterval.emit()


def sendWhatsAppMessage(message: str)->None:
    try:
        pyw.sendwhatmsg_to_group_instantly(
            "Eg2FrFoCjZG2BZLUCKp9xL",
            message,
        )
        print("Message sent!")
    except Exception as e:
        print(str(e))