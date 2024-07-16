from typing import Literal

from utils.alert_model import AlertDataModel
from utils.signal_bus import signalBus


def API_dispatchAlert(msg: str, mode: Literal["error", "warning", "event"] = 'error'):
    alert = AlertDataModel(msg, mode)
    signalBus.writeToConsole.emit(alert)
