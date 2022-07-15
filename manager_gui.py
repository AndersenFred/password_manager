from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import getpass
import password_manager as pm
import sys

class manager_gui(QWidget):
    class button(QWidget):
        def __init__(self, zugehörigkeit, name:str,  connection, position, tag:str = None):
            x = QPushButton(name, zugehörigkeit)
            x.move(*position)
            x.clicked.connect(connection)
            if (tag != None):
                x.setToolTip(tag)

    def __init__(self):
        self.masterPw_correct = False
        super().__init__()
        self.keys = []
        self.manager = pm.manager()
        self.init()

    def add_Button(self, name:str,  connection, position, tag:str = None):
        return self.button(self, name,  connection, position, tag)

    def init(self):
        self.add_Button('Masterpasswort', self.checkmasterPW, (250,50), 'Überprüft ob das Masterpasswort stimmt')
        self.add_Button('Neues Passwort hinzufügen', self.newPW, (250, 100), 'Fügt ein neues Passwort hinzu')
        self.add_Button('Passwort generieren', self.generator, (250, 150), 'Generiert ein 64 zeichen langes Passwort')
        self.add_Button('Refresh', self.refresh,(250, 250), 'Läd die gespeicherten Passwörter neu')
        self.add_Button('Browse', self.filePath_press,(250,200), 'Öffnet den Dateiexplorer zur Auswahl der Speicherungsdatei')
        self.add_Button('Neuen Manager anlegen', self.newManager,(100,300), 'Erzeugt eine neue Speicherungsdatei.\nÜberschreibt bereits bestehende Dateien')
        self.add_Button('Exit', self.exit, (250,300),'Beendet das Programm')

        self.masterPW = QLineEdit(self)
        self.masterPW.setEchoMode(QLineEdit.EchoMode.Password)
        self.masterPW.move(100,50)
        self.masterPW.textChanged.connect(self.masPW_change)
        self.masterPW.setToolTip('Zur eingabe des Masterpasswort')

        self.combobox_pw = QComboBox(self)
        self.combobox_pw.move(100,250)
        self.combobox_pw.setFixedWidth(130)
        self.combobox_pw.currentIndexChanged.connect(self.read_pw)
        self.combobox_pw.setToolTip('Zur Auswahl des Passworts')

        self.add_pw_key = QLineEdit(self)
        self.add_pw_key.move(100,100)
        self.add_pw_key.setToolTip('Eingabe der Passwortquelle')

        self.add_pw = QLineEdit(self)
        self.add_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.add_pw.move(100,150)
        self.add_pw.setToolTip('Eingabe des neuen Passworts')

        self.pw_gen_len = QSpinBox(self)
        self.pw_gen_len.move(50,150)
        self.pw_gen_len.setValue(64)


        self.filePath = QLineEdit(self)
        self.filePath.move(100,200)
        self.filePath.setToolTip('Auswahl der Zieldatei')
        self.refresh()

    def masPW_change(self):
        self.masterPw_correct = False

    def exit(self):
        self.manager.save()
        sys.exit()

    def read_pw(self, index):
        index = self.combobox_pw.currentText()
        try:
            if(self.masterPw_correct):
                self.manager.read_password(index)
            elif (self.masterPW.text() != ''):
                reply = QMessageBox()
                reply.setText('Es muss erst das Masterpasswort validiert werden')
                reply.setStandardButtons(QMessageBox.StandardButton.Ok)
                reply.exec()
        except KeyError:
            pass
        except UnicodeDecodeError:
            if (self.masterPW.text() != ''):
                reply = QMessageBox()
                reply.setText('Es ist beim decodieren ein Fehler aufgetreten')
                reply.setStandardButtons(QMessageBox.StandardButton.Ok)
                reply.exec()

    def checkmasterPW(self):
        self.manager.start(self.masterPW.text(), self.filePath.text())
        try:
            if (self.manager.checkmasterPW(self.masterPW.text())):
                reply = QMessageBox()
                reply.setText('Masterpasswörter stimmen überein')
                reply.setStandardButtons(QMessageBox.StandardButton.Ok)
                reply.exec()
                self.masterPw_correct = True
                self.refresh()
            else:
                reply = QMessageBox()
                reply.setText('Masterpasswörter stimmen nicht überein')
                reply.setStandardButtons(QMessageBox.StandardButton.Ok)
                reply.exec()
                self.masterPw_correct = False
        except KeyError:
            reply = QMessageBox()
            reply.setText('Es muss erst ein Dateipfad ausgewählt werden')
            reply.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply.exec()

    def generator(self):

        x = pm.manager.generator(self.pw_gen_len.value())
        self.add_pw.setText(x)

    def refresh(self):
        if self.masterPw_correct:
            self.manager.initialisiere()
            self.combobox_pw.clear()
            try:
                self.keys = self.manager.data.keys()
                for i in self.keys:
                    if i != 'masterPassword':
                        self.combobox_pw.addItem(i)
            except NameError:
                pass

    def newPW(self):
        if self.add_pw_key.text()=='':
            reply = QMessageBox()
            reply.setText('Es muss erst eine Quelle für das Passwort eingegeben werden')
            reply.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply.exec()
            return
        if (self.add_pw_key.text() in self.manager.data):
            reply = QMessageBox()
            reply.setText('Zu dieser Quelle gibt es bereits ein Passwort.\nÜberschreiben?')
            reply.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
            x = reply.exec()
            if x == QMessageBox.StandardButton.No:
                return
        if len(self.add_pw.text()) < 10:
            reply = QMessageBox()
            reply.setText('das passwort ist sehr kurz.\nTrozudem weiter?')
            reply.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            x = reply.exec()
            if x == QMessageBox.StandardButton.No:
                return
        if  (not self.masterPw_correct):
            reply = QMessageBox()
            reply.setText('Das Masterpasswort muss erst validiert werden')
            reply.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply.exec()
            return
        try:
            self.manager.add_password(self.add_pw_key.text(), self.add_pw.text())
            self.refresh()
        except FileNotFoundError:
            reply = QMessageBox()
            reply.setText('Es muss erst ein Dateipfad ausgewählt werden')
            reply.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply.exec()

    def filePath_press(self):
        fd = QFileDialog()
        self.fileName = fd.getOpenFileName(self,'Open', f'C:\\Users\{getpass.getuser()}\Desktop', '(*.json)')
        self.filePath.setText(self.fileName[0])
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
            reply.setStandardButtons(QMessageBox.StandardButton.Ok )
            x = reply.exec()
            self.refresh()
