from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import getpass
import password_manager as pm
import sys

class manager_gui(QWidget):
    def __init__(self):
        super().__init__()
        self.keys = []
        self.manager = pm.manager()
        self.init()


    def init(self):
        self.masterPW = QLineEdit(self)
        self.masterPW.setEchoMode(QLineEdit.EchoMode.Password)
        self.masterPW.move(100,200)
        checkermasterPW =  QPushButton('Masterpassword', self)
        checkermasterPW.move(250, 200)
        checkermasterPW.clicked.connect(self.checkmasterPW)
        self.w = QComboBox(self)
        self.w.move(100,150)
        self.w.setFixedWidth(130)
        self.add_pw_key = QLineEdit(self)
        self.add_pw_key.move(100,50)
        self.add_pw = QLineEdit(self)
        self.add_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.add_pw.move(100,100)
        create_new_password = QPushButton('Neues Passwort hinzufügen', self)
        create_new_password.move(250, 50)
        create_new_password.clicked.connect(self.newPW)
        generator = QPushButton('Passwort generieren', self)
        generator.move(250, 100)
        generator.clicked.connect(self.generator)
        refre = QPushButton('refresh', self)
        refre.move(100, 450)
        refre.clicked.connect(self.refresh)
        create_new_manager = QPushButton('Neuen Manager anlegen', self)
        create_new_manager.move(250,150)
        create_new_manager.clicked.connect(self.newManager)
        self.refresh()
        self.filePath = QLineEdit(self)
        self.filePath.move(100,250)
        filePath_Button = QPushButton('Browse', self)
        filePath_Button.move(250,250)
        filePath_Button.clicked.connect(self.filePath_press)

    def checkmasterPW(self):
        print(self.manager.checkmasterPW(self.masterPW.text()))
        if (self.manager.checkmasterPW(self.masterPW.text())):
            reply = QMessageBox()
            reply.setText('Masterpasswörter stimmt überein')
            reply.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply.exec()
        else:
            reply = QMessageBox()
            reply.setText('Masterpasswörter stimmen nicht überein')
            reply.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply.exec()

    def generator(self):
        x = pm.manager.generator(64)
        self.add_pw.setText(x)

    def refresh(self):
        self.manager.initialisiere()
        self.w.clear()
        try:
            self.keys = self.manager.data
            for i in self.keys.keys():
                print(type(i))
                self.w.addItem(i)
        except NameError:
            print('ATterr')

    def newPW(self):
        self.manager.add_password(self.add_pw_key.text(), self.add_pw.text())
        self.refresh()

    def filePath_press(self):
        fd = QFileDialog()
        self.fileName = fd.getOpenFileName(self,'Open', f'C:\\Users\{getpass.getuser()}\Desktop', '(*.json)')
        self.filePath.setText(self.fileName[0])
        self.manager.start(self.masterPW.text(), self.filePath.text())
        self.refresh()

    def newManager(self):
        try:
            if (self.filePath.text()==''):
                raise AttributeError
            reply = QMessageBox()
            reply.setText('Bestehende Dateien werden überschrieben\nDies kann nicht rückgängig gemacht werden')
            reply.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            x = reply.exec()
            if(x == QMessageBox.StandardButton.Yes):
                self.manager.masterPassword_setter(self.masterPW.text())
                self.manager.create_new_manager()
                self.refresh()
        except AttributeError:
            reply = QMessageBox()
            reply.setText('Es muss erst ein Dateipfad ausgewählt werden')
            reply.setStandardButtons(QMessageBox.StandardButton.Yes )
            x = reply.exec()
            self.refresh()
