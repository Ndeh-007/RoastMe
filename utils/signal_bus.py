from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    writeToConsole = Signal(object)
    initializeApplicationData = Signal()

    onReduceBubble = Signal()
    onConfigureApplication = Signal()
    onTerminateApplication = Signal()
    onHideBubble = Signal()

    onEnlargeWindow = Signal(object)


signalBus = SignalBus()
