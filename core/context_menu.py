from core.signalBus import signalBus


def quit_application():
    signalBus.onCloseWindow.emit()


def open_settings():
    print("setting")
