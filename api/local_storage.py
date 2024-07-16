import warnings
from typing import Any

from core.app_settings import LOCAL_STORAGE, StorageEntity
from utils.exception_handler import exception_warning_handler


def API_InitializeLocalStorage():
    """
    primes the local storage
    :return:
    """
    LOCAL_STORAGE.prime()


@exception_warning_handler("api")
def API_fetchAppSettings() -> dict[str, StorageEntity]:
    """
    fetches all the app settings
    :return:
    """
    return LOCAL_STORAGE.opts()


@exception_warning_handler("api")
def API_fetchAppSettingsItem(target: str, value=True) -> None | StorageEntity | Any:
    """
    given a particular key, it returns the storage entity value of that key if found, otherwise None
    if value is False, returns the storage entity of that key
    :param target:
    :param value:
    :return:
    """

    se = LOCAL_STORAGE.opts().get(target)

    # if we want the storage entity
    if not value:
        return se

    # if we want the value of the storage entity
    if se is None:
        return se

    # otherwise, get the storage entity value
    return se.value()


@exception_warning_handler("api")
def API_UpdateAppSettings(data: dict[str, StorageEntity] | dict[str, Any]):
    """
    updates the value of data in the local storage.
    if the keys do not exist, new values are created for them
    :param data:
    :return:
    """
    if data is None:
        warnings.warn('Cannot Update App Settings with NoneType')
        return False

    for k, v in data.items():
        if isinstance(v, StorageEntity):
            LOCAL_STORAGE.opts().update({k: v})
        else:
            LOCAL_STORAGE.opts().update({k: StorageEntity(k, v)})

    return True
