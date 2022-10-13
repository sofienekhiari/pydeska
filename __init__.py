import os
from aqt import mw
from aqt.deckbrowser import DeckBrowser
from aqt.utils import qconnect
from aqt.qt import *
from anki.decks import DeckManager

def load_sk_style():
    qss_file_name = os.getcwd() + "/skqss"
    with open(qss_file_name, "r") as qss_file:
        return qss_file.read()

class AddMultipleDecks(QMainWindow):
    def __init__(self):
        super().__init__(mw)
        self.setWindowTitle("Add multiple decks")
        self.setGeometry(100, 100, 500, 400)
        self.pd_label = QLabel("Parent deck:")
        self.pd_text = QLineEdit()
        self.pd_text.setToolTip("Leave empty if you don't need one")
        self.cd_label = QLabel("Children decks:")
        self.cd_text = QTextEdit()
        self.cd_text.setToolTip("Add every deck title on a different line")
        self.amd_submit_button = QPushButton("Create")
        self.amd_submit_button.clicked.connect(self.add_multiple_decks)
        layout = QVBoxLayout()
        layout.addWidget(self.pd_label)
        layout.addWidget(self.pd_text)
        layout.addWidget(self.cd_label)
        layout.addWidget(self.cd_text)
        layout.addWidget(self.amd_submit_button, alignment=Qt.AlignmentFlag.AlignRight)
        amd_window_central_widget = QWidget()
        amd_window_central_widget.setLayout(layout)
        amd_window_central_widget.setStyleSheet(load_sk_style())
        self.setCentralWidget(amd_window_central_widget)

    def add_multiple_decks(self):
        pd_text = self.pd_text.text()
        cd_original_list = self.cd_text.toPlainText().split("\n")
        cd_list = [
            cd_text if pd_text == "" else pd_text + "::" + cd_text
            for cd_text in cd_original_list
        ]
        amd_browser = DeckBrowser(mw)
        amd_manager = DeckManager(mw.col)
        for cd_deck in cd_list:
            amd_manager.add_normal_deck_with_name(cd_deck)
        amd_browser.refresh()
        self.hide()


def add_multiple_decks_window():
    amd_window = AddMultipleDecks()
    amd_window.show()


amd_action = QAction("Add multiple decks", mw)
qconnect(amd_action.triggered, add_multiple_decks_window)
mw.form.menuTools.addAction(amd_action)
