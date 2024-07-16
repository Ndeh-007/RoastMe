from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout


class VSettingsGroupItem(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)

        # define body
        w = QWidget()
        self.sgLayout = QGridLayout()
        # self.sgLayout.setContentsMargins(0, 0, 0, 0)
        w.setLayout(self.sgLayout)
        w.setObjectName("VSettingsGroupItemBody")

        # define main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # append contents
        layout.addWidget(w)

        # attach to widget
        self.setLayout(layout)
        self.setObjectName('VSettingsGroupItemBody')

        # self.setStyleSheet(
        #     """
        #         QWidget#VSettingsGroupItemBody{
        #             border-width: 0px 0px 0.5px 0px;
        #             border-color: #c0c2c4;
        #             border-style: solid;
        #         }
        #     """
        # )

    def addWidget(self, w: QWidget, row: int, col: int = 0, rowSpan: int = 1, colSpan: int = 1):
        self.sgLayout.addWidget(w, row, col, rowSpan, colSpan)
