import password_manager as pm
import manager_GUI as mg
import sys
from PyQt6.QtWidgets import QApplication


if __name__ == '__main__':
    w = QApplication(sys.argv)
    app = mg.manager_gui()
    app.show()
    w.exec()
    app.manager.save()
