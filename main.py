from modules import manager_GUI as mg
import sys
from PyQt6.QtWidgets import QApplication


if __name__ == '__main__':
    w = QApplication(sys.argv)
    app = mg.manager_gui()
    app.show()
    w.exec()
    if app.manager.file != '' and app.masterPw_correct:
        app.manager.save()
