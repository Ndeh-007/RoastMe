from PySide6 import QtCore
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit, QComboBox, QCheckBox, QLabel, QDialog

from api.alerts import API_dispatchAlert
from api.local_storage import API_UpdateAppSettings, API_fetchAppSettings
from core.config_variables import APP_NAME
from models.storage_entity import StorageEntity
from utils.exception_handler import exception_warning_handler
from utils.helpers import getIndexFromComboBoxWithData, non_overlapping_strings, populateComboBox
from utils.signal_bus import signalBus
from views.settings.console import VConsole
from views.settings.settings_group_item import VSettingsGroupItem


class VSettingsView(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)

        self.__init_ui()
        self.__prime_ui()
        self.__init_window_attrib__()

        self.__config_ui()

        self.connectSignals()

    # region initialize
    def __init_window_attrib__(self):

        self.setWindowTitle(f"{APP_NAME} - Settings")
        self.setWindowIcon(QIcon(":/images/roast_me.ico"))
        self.setWindowFlag(QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint, True)
        self.setModal(False)

    def __init_ui(self):
        """
        creates the various ui components
        :return:
        """
        self.label = QLabel("Settings")
        self.console = VConsole()
        self.durationInput = QLineEdit()
        self.languageComboBox = QComboBox()
        self.categoryComboBox = QComboBox()

        self.categoryOptions = {
            "Programming": QCheckBox("Programming"),
            "Misc": QCheckBox("Misc"),
            "Dark": QCheckBox("Dark"),
            "Pun": QCheckBox("Pun"),
            "Spooky": QCheckBox("Spooky"),
            "Christmas": QCheckBox("Christmas"),
        }

        self.jokeFlagsOptions = {
            "nsfw": QCheckBox("nsfw"),
            "religious": QCheckBox("religious"),
            "political": QCheckBox("political"),
            "racists": QCheckBox("racists"),
            "sexist": QCheckBox("sexist"),
            "explicit": QCheckBox("explicit"),
        }

        self.jokeTypeOptions = {
            "single": QCheckBox("single"),
            "twopart": QCheckBox("twopart"),
        }

        # create holders

        # time
        self.t_so = VSettingsGroupItem()
        self.t_so.addWidget(QLabel('Fetch Duration (min)'), 0, 0)
        self.t_so.addWidget(self.durationInput, 0, 1)
        self.t_so.addWidget(QLabel('Language'), 0, 2)
        self.t_so.addWidget(self.languageComboBox, 0, 3)
        self.t_so.addWidget(QWidget(), 0, 4)
        self.t_so.sgLayout.setColumnStretch(4, 1)

        # category
        self.c_so = VSettingsGroupItem()
        self.c_so.addWidget(QLabel('Joke Category'), 0, 0)
        self.c_so.addWidget(self.categoryComboBox, 0, 1)
        self.c_so.addWidget(QWidget(), 0, 2)
        self.c_so.sgLayout.setColumnStretch(2, 1)

        for i, (k, w) in enumerate(self.categoryOptions.items()):
            self.c_so.addWidget(w, 1, int(i) + 1)

        # flags
        self.jf_so = VSettingsGroupItem()
        self.jf_so.addWidget(QLabel("Filter out: "), 0, 0)
        self.jf_so.addWidget(QWidget(), 0, 2)
        for i, (k, w) in enumerate(self.jokeFlagsOptions.items()):
            self.jf_so.addWidget(w, 1, int(i) + 1)

        # types
        self.jt_so = VSettingsGroupItem()
        self.jt_so.addWidget(QLabel('Joke Type: '), 0, 0)
        self.jt_so.addWidget(QWidget(), 0, 2)
        self.jt_so.sgLayout.setColumnStretch(2, 1)

        for i, (k, w) in enumerate(self.jokeTypeOptions.items()):
            self.jt_so.addWidget(w, 1, int(i) + 1)

        layout = QGridLayout()
        layout.addWidget(QWidget(), 0, 0)
        layout.addWidget(self.label, 0, 1, )
        layout.addWidget(self.t_so, 1, 1)
        layout.addWidget(self.c_so, 2, 1)
        layout.addWidget(self.jf_so, 4, 1)
        layout.addWidget(self.jt_so, 5, 1)
        layout.addWidget(QWidget(), 5, 2)
        layout.addWidget(self.console, 6, 1)
        layout.addWidget(QWidget(), 7, 0)

        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 3)
        layout.setRowStretch(7, 1)

        layout.setVerticalSpacing(20)

        self.setLayout(layout)

    def __prime_ui(self):
        """
        attaches their default values
        :return:
        """
        opts = {
            "Any": "any",
            "Custom": "custom"
        }
        populateComboBox(self.categoryComboBox, opts)
        self.__setCategoryOptionsDisable(True)

        opts = {
            "en - English": "en",
            "fr - French": "fr",
        }
        populateComboBox(self.languageComboBox, opts)

    def __config_ui(self):
        """
        connects the signal and slots to various sections
        :return:
        """
        self.durationInput.editingFinished.connect(self.__handleDurationInputFinished)
        self.languageComboBox.currentIndexChanged.connect(self.__handleLanguageChanged)
        self.categoryComboBox.currentIndexChanged.connect(self.__categoryModeChanged)

        for box in self.categoryOptions.values():
            box.checkStateChanged.connect(self.__handleJokeCategoryChanged)

        for box in self.jokeFlagsOptions.values():
            box.checkStateChanged.connect(self.__handleJokeFlagsChanged)

        for box in self.jokeTypeOptions.values():
            box.checkStateChanged.connect(self.__handleJokeTypeChanged)

    def __prime_ui_content(self):
        """
        loads content from the local storage and adjusts the ui
        :return:
        """
        opts: dict[str, StorageEntity] = API_fetchAppSettings()

        # duration
        self.durationInput.setText(str(opts.get('fetch_interval').value()))

        # language
        lang = opts.get('joke_language').value()
        idx = getIndexFromComboBoxWithData(self.languageComboBox, lang)
        if idx is not None:
            self.languageComboBox.setCurrentIndex(idx)

        def changeCheckBoxOptsState(dataOpts: str, dataset: dict[str, QCheckBox]):
            dataOpts = dataOpts.split(",")
            if len(dataOpts) == 0:
                pass
            else:
                outliers = non_overlapping_strings(dataOpts, list(dataset.keys()))
                for _opts in dataOpts:
                    box = dataset.get(_opts)
                    box.setChecked(True)

                for _opts in outliers:
                    box = dataset.get(_opts)
                    box.setChecked(False)

        # joke_category
        catOpts = opts.get('joke_category').value()
        if isinstance(catOpts, str):
            if catOpts == "Any":
                self.categoryComboBox.setCurrentIndex(0)
            else:
                self.categoryComboBox.setCurrentIndex(1)
                changeCheckBoxOptsState(catOpts, self.categoryOptions)

        # joke flags
        catOpts = opts.get('joke_flags').value()
        if isinstance(catOpts, str):
            changeCheckBoxOptsState(catOpts, self.jokeFlagsOptions)

        # joke type
        catOpts = opts.get('joke_type').value()
        if isinstance(catOpts, str):
            changeCheckBoxOptsState(catOpts, self.jokeTypeOptions)

    # endregion

    # region event handling
    @exception_warning_handler("settings")
    def __handleLanguageChanged(self, index: int):
        data = self.languageComboBox.itemData(index)
        self.dispatchToStorage({"joke_language": data})

    @exception_warning_handler("settings")
    def __handleJokeTypeChanged(self, _=None):
        catOpts = self.__collectCheckBoxOptions(self.jokeTypeOptions)
        if catOpts is None:
            catOpts = "jokes,insults"
        self.dispatchToStorage({"joke_flags": catOpts})

    @exception_warning_handler("settings")
    def __handleJokeFlagsChanged(self, _=None):
        catOpts = self.__collectCheckBoxOptions(self.jokeFlagsOptions)
        self.dispatchToStorage({"joke_flags": catOpts})

    @exception_warning_handler("settings")
    def __handleJokeCategoryChanged(self, _=None):
        """

        :param _:
        :return:
        """
        catOpts = self.__collectCheckBoxOptions(self.categoryOptions)
        if catOpts is None:
            # if no box is checked, fire warning. set category to any
            API_dispatchAlert("Under custom mode, a category must be selected.Defaulting to any", "warning")
            self.categoryComboBox.setCurrentIndex(0)
            return

        self.dispatchToStorage({"joke_category": catOpts})

    @exception_warning_handler("settings")
    def __categoryModeChanged(self, index: int):
        data = self.categoryComboBox.itemData(index)

        if data == "any":
            self.__setCategoryOptionsDisable(True)
            self.dispatchToStorage({"joke_category": "Any"})

        if data == "custom":
            self.__setCategoryOptionsDisable(False)
            catOpts = self.__collectCheckBoxOptions(self.categoryOptions)

            if catOpts is None:  # no box is checked

                # force check all boxes
                for box in self.categoryOptions.values():
                    box.setChecked(True)

                # collect data and dispatch
                catOpts = self.__collectCheckBoxOptions(self.categoryOptions)
            self.dispatchToStorage({"joke_category": catOpts})

    @exception_warning_handler("settings")
    def __handleDurationInputFinished(self):
        text = self.durationInput.text()
        value = 15
        try:
            value = float(text)
        except Exception as e:
            API_dispatchAlert(f"value must be number")
            self.durationInput.setText(f"{value}")
            return

        if value <= 0:
            API_dispatchAlert("Cannot have an interval of 0 mins. Defaulting to 1 min", "warning")
            value = 1
            self.durationInput.setText(f"{value}")

        self.dispatchToStorage({"fetch_interval": str(value)})

    def __handleConfigure(self):
        self.launch()
    # endregion

    # region override

    # endregion

    # region worker
    def launch(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def __collectCheckBoxOptions(self, dataset: dict[str, QCheckBox]) -> str | None:
        txt = ""
        for k, box in dataset.items():
            if box.isChecked():
                txt += f"{k},"

        if len(txt) == 0:  # if no box is checked
            return None

        if len(txt) > 0:
            txt = txt[:-1]  # remove the last comma

        return txt

    def __setCategoryOptionsDisable(self, state: bool):
        for box in self.categoryOptions.values():
            box.setDisabled(state)

    def dispatchToStorage(self, opts: dict[str, object]):
        state = API_UpdateAppSettings(opts)
        if not state:
            API_dispatchAlert(f"Failed to update.")
        else:
            API_dispatchAlert(f"Change Successful.", "event")

        return state

    # endregion

    # region connect signals

    def connectSignals(self):
        signalBus.initializeApplicationData.connect(self.__prime_ui_content)
        signalBus.onConfigureApplication.connect(self.launch)

    # endregion
