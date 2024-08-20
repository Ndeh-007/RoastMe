from PySide6.QtWidgets import QComboBox
import re


def reading_time(text: str, WPM: int = 200):
    """
    computes the time taken to read the number of words
    :param text:
    :param WPM:
    :return:
    """
    words = text.split()
    nWords = len(words)
    return nWords/WPM


def mins_to_ms(value: float, castToInt=False):
    """
    converts minutes to milliseconds
    :param value:
    :param castToInt:
    :return:
    """

    if castToInt:
        return int(value * 60000)

    return value * 60000


def populateComboBox(box: QComboBox, data: dict[str, str]):
    """
    appends data to a combo box
    :param box:
    :param data:
    :return:
    """

    for k, v in data.items():
        box.addItem(k, v)


def getIndexFromComboBoxWithData(box: QComboBox, data: object) -> int | None:
    """
    finds the index of an item in a combox box via the provided data
    :param box:
    :param data:
    :return:
    """
    for i in range(box.count()):
        _data = box.itemData(i)
        if _data == data:
            return i

    return None


def non_overlapping_strings(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)

    # Strings that are in arr1 but not in arr2
    only_in_arr1 = set1 - set2

    # Strings that are in arr2 but not in arr1
    only_in_arr2 = set2 - set1

    # Combine the non-overlapping strings
    non_overlapping = list(only_in_arr1) + list(only_in_arr2)

    return non_overlapping
