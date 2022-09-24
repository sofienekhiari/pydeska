from aqt import mw
from aqt.utils import qconnect
from aqt.qt import *

def add_multiple_decks():
    pass

amd_action = QAction("Add multiple decks", mw)
qconnect(amd_action.triggered, add_multiple_decks)
mw.form.menuTools.addAction(amd_action)
