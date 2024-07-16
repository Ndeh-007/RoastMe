import os.path

from core.config_variables import CONFIG_FILE
from models.storage_entity import StorageEntity
from utils.file_readers import write_config_file, read_config_file
from utils.logger import Logger


class LocalStorage:

    def __init__(self):

        self.__opts: dict[str, StorageEntity] = {}
        self.__logger = Logger("local_storage")

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
            "fetch_interval": StorageEntity("fetch_interval", 15),
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

    def opts(self):
        return self.__opts


LOCAL_STORAGE = LocalStorage()
