from PySide6.QtCore import QObject, Signal, QSize


class SignalBus(QObject):
    onCloseWindow = Signal()
    onEnlargeWindow = Signal(QSize)
    onReduceWindow = Signal()


signalBus = SignalBus()
