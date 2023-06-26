from time import sleep

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
