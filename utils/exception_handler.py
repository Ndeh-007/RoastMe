import sys
import warnings

from typing import Literal

from utils.alert_model import AlertDataModel
from utils.logger import Logger
from utils.signal_bus import signalBus


def dispatch_to_ui(msg: str, mode: Literal["error", "warning", "event"] = "error"):
    model = AlertDataModel(msg, mode)
    signalBus.writeToConsole.emit(model)


def exception_warning_handler(log: str = 'global', *default):
    """
    A decorator to handle warnings and errors that happens in functions. For each warning or except caught,
    1. It writes them to the designated log file
    2. Dispatches them to the UI
    @param log: the name of the log file to be written to, defaults to "global", if no name is provided
    @param default: the default arguments returned by the function
    @return:
    """

    def outer(func):
        def inner(*args, **kwargs):
            try:
                with warnings.catch_warnings(record=True) as caught_warnings:
                    result = func(*args, **kwargs)
                    for warning in caught_warnings:
                        print(f"A warning occurred: {warning.message}")
                        Logger(log).warning(warning.message)
                        dispatch_to_ui(warning.message, "warning")
                    return result
            except Exception as e:
                print(f"An error occurred: {e}")
                Logger(log).error(e, sys.exc_info())
                dispatch_to_ui(f"An error occurred: {e}", "error")
        return inner

    return outer
