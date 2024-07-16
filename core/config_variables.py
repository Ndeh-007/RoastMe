from pathlib import Path

from PySide6.QtCore import QStandardPaths

DEBUG = True

YEAR = 2023
AUTHOR = "NDEH.AKUMAH"
VERSION = "2.0.0"
APP_NAME = "HumorMe"
EXEC_DIR = Path(__file__).parent
BASE_DIR = EXEC_DIR.parent


if DEBUG:
    CONFIG_FOLDER = Path('AppData').absolute()
else:
    CONFIG_FOLDER = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)) / APP_NAME

CONFIG_FILE = CONFIG_FOLDER / "config.xml"

