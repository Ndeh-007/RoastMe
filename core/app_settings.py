import os.path

from PySide6.QtCore import QObject, QTimer

from core.config_variables import CONFIG_FILE
from models.storage_entity import StorageEntity
from utils.common_variables import BASE_INSULTS_URL, BASE_JOKES_URL
from utils.file_readers import write_config_file, read_config_file
from utils.logger import Logger


class LocalStorage(QObject):
    pointer = 0

    def __init__(self):
        super().__init__()

        self.__opts: dict[str, StorageEntity] = {}
        self.__logger = Logger("local_storage")

        self.__jokesURL: str = f"{BASE_JOKES_URL}Any?format=txt"
        self.__insultsURL: str = f"{BASE_INSULTS_URL}generate_insult.php?lang=en&type=json"

        self.__autoSaveTimer = QTimer()
        self.__autoSaveTimer.setInterval(2000)  # 2 secs
        self.__autoSaveTimer.setSingleShot(True)
        self.__autoSaveTimer.timeout.connect(lambda: write_config_file(self.__opts, CONFIG_FILE))

    # region initialize
    def prime(self):
        """
        prepares the local storage for usage
        :return:
        """
        try:
            if os.path.exists(CONFIG_FILE):
                self.__initializeFromFile(CONFIG_FILE)
            else:
                self.__initialize()

            self.constructAPIURLS()
        except Exception as e:
            self.__logger.error(e, True)

    def __initializeFromFile(self, path: str):
        """
        populates the storage with data from the config file
        :return:
        """
        opts = read_config_file(path)
        self.__opts.update(opts)

    def __initialize(self):
        """
        populations the storage data with empty values and creates the
        config file

        see items description here: https://jokeapi.dev/
        :return:
        """
        opts = {
            "fetch_interval": StorageEntity("fetch_interval", 15),  # minutes
            "bubble_display_time": StorageEntity("bubble_display_time", 0.25),  # minutes
            "joke_language": StorageEntity("joke_language", "en"),
            "joke_category": StorageEntity("joke_category", "Any"),
            "joke_flags": StorageEntity("joke_flags", None),
            "joke_type": StorageEntity("joke_type", "single,twopart"),
            "joke_quantity": StorageEntity("joke_quantity", 1),
            "fetch_mode": StorageEntity("fetch_mode", "jokes,insults")  # fetch both insults and jokes
        }

        # updates the local storage
        self.__opts.update(opts)

        # saves the storage file
        write_config_file(opts, CONFIG_FILE)

    # endregion

    # region getters
    def opts(self):
        return self.__opts

    def jokesURL(self):
        return self.__jokesURL

    def insultsURL(self):
        return self.__insultsURL

    # endregion

    # region workers
    def triggerSaveTimer(self):
        self.__autoSaveTimer.start()

    def constructAPIURLS(self):
        """
        builds the fetching urls based on the settings
        :return:
        """

        # region jokes
        url = f"{BASE_JOKES_URL}"

        # append the categories
        _categories = self.__opts.get("joke_category").value()
        url += _categories

        # append the language
        _lang = self.__opts.get("joke_language").value()
        url += f"?lang={_lang}"

        # append the filters
        _flags = self.__opts.get("joke_flags").value()
        if _flags is not None:
            url += f"&blacklistFlags={_flags}"

        # append the type
        _jType = self.__opts.get('joke_type').value()
        url += f"&type={_jType}"

        # append the joke amount
        _amt = self.__opts.get('joke_quantity').value()
        url += f"&amount={int(_amt)}"

        # collect constructed url
        self.__jokesURL = url

        # endregion

    # endregion


LOCAL_STORAGE = LocalStorage()
