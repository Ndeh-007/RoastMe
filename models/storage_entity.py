from typing import Any


class StorageEntity:
    """
    holds values of the various application settings
    """

    def __init__(self, key: str, value: Any = None):
        self.__key = key
        self.__value = value

    # region setters
    def setKey(self, key):
        self.__key = key

    def setValue(self, value):
        self.__value = value

    # endregion

    # region getters
    def key(self):
        return self.__key

    def value(self):
        return self.__value

    # endregion

    # region workers
    def reset(self):
        self.__value = None
    # endregion

