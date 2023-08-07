from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import getpass
import modules.password_manager as pm
import sys
import os
import hashlib

class manager_gui(QWidget):
    class button(QWidget):
        def __init__(self, zugehoerigkeit, name:str,  connection, position, tag:str = None):
            x = QPushButton(name, zugehoerigkeit)
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
        self.setGeometry(50,50,550,400)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle('Passwortmanager')
        self.add_Button('Masterpasswort', self.checkmasterPW, (250,50), 'Überprüft ob das Masterpasswort stimmt')
        self.add_Button('Neues Passwort hinzufügen', self.newPW, (250, 100), 'Fügt ein neues Passwort hinzu')
        self.add_Button('Passwort generieren', self.generator, (250, 150), 'Generiert ein 64 zeichen langes Passwort')
        #self.add_Button('Refresh', self.refresh,(0, 250), 'Läd die gespeicherten Passwörter neu')
        self.add_Button('Browse', self.filePath_press,(250,200), 'Öffnet den Dateiexplorer zur Auswahl der Speicherungsdatei')
        self.add_Button('Neuen Manager anlegen', self.newManager,(100,300), 'Erzeugt eine neue Speicherungsdatei.\nÜberschreibt bereits bestehende Dateien')
        self.add_Button('Exit', self.exit, (250,300),'Beendet das Programm')
        self.add_Button('Passwort kopieren', self.read_pw,(250,250),'Kopiert das ausgewählte Passwort in die Zwischenablage')
        self.add_Button('Masterpasswort ändern', self.change_master_pw,(350,50),'Aktualisiert das Masterpasswort, das alte muss eingegebern sein.')
        self.masterPW = QLineEdit(self)
        self.masterPW.setEchoMode(QLineEdit.EchoMode.Password)
        self.masterPW.move(100,50)
        self.masterPW.textChanged.connect(self.masPW_change)
        self.masterPW.setToolTip('Zur eingabe des Masterpasswort')

        self.combobox_pw = QComboBox(self)
        self.combobox_pw.move(100,250)
        self.combobox_pw.setFixedWidth(130)
        self.combobox_pw.setToolTip('Zur Auswahl des Passworts')

        self.add_pw_key = QLineEdit(self)
        self.add_pw_key.move(100,100)
        self.add_pw_key.setToolTip('Eingabe der Passwortquelle')

        self.add_pw = QLineEdit(self)
        self.add_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.add_pw.move(100,150)
        self.add_pw.setToolTip('Eingabe des neuen Passworts')

        self.pw_gen_len = QSpinBox(self)
        self.pw_gen_len.move(40,150)
        self.pw_gen_len.setValue(64)
        self.pw_gen_len.setFixedWidth(50)
        self.pw_gen_len.setToolTip('Legt die länge des genergierten Passworts fest')
        self.pw_gen_len.setMaximum(1024)
        self.pw_gen_len.setMinimum (1)

        self.filePath = QLineEdit(self)
        self.filePath.move(100,200)
        self.filePath.setToolTip('Auswahl der Zieldatei')
        self.refresh()

    def masPW_change(self):
        self.masterPw_correct = False
        self.refresh()

    def exit(self):
        self.refresh()
        if not self.masterPw_correct and not self.filePath.text() == '':
            reply = QMessageBox()
            reply.setText('Das Masterpasswort ist nicht validiert, änderungen werden evlt. nicht gespeichert.\n Trotzdem schließen?')
            reply.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
            x = reply.exec()
            if x == QMessageBox.StandardButton.No:
                return
            else:
                sys.exit()
        self.manager.save()
        sys.exit()

    def read_pw(self):
        index = self.combobox_pw.currentText()
        self.refresh()
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
        self.refresh()

    def checkmasterPW(self):
        self.refresh()
        self.manager.start(self.masterPW.text(), self.filePath.text())
        try:
            if (self.manager.checkmasterPW(self.masterPW.text())):
                reply = QMessageBox()
                reply.setText('Masterpasswörter stimmen überein')
                reply.setStandardButtons(QMessageBox.StandardButton.Ok)
                reply.exec()
                self.masterPw_correct = True
            else:
                reply = QMessageBox()
                reply.setText('Masterpasswörter stimmen nicht überein')
                reply.setStandardButtons(QMessageBox.StandardButton.Ok)
                reply.exec()
                self.masterPw_correct = False
        except KeyError:
            name, ok = QInputDialog.getText(self, 'Dateiname', 'Bitte geb den Dateinamen ein:')
            if not ok:
                return
            self.filePath.setText(f'C:\\Users\{getpass.getuser()}\AppData\Roaming\.cookies_pw_manager\{name}')
            if os.path.isdir(f'C:\\Users\{getpass.getuser()}\AppData\Roaming\.cookies_pw_manager\ '):
                if os.path.isfile(name):
                    self.refresh
                    return
                else:
                    self.newManager(name, f'C:\\Users\{getpass.getuser()}\AppData\Roaming\.cookies_pw_manager')
            else:
                os.makedirs(f'C:\\Users\{getpass.getuser()}\AppData\Roaming\.cookies_pw_manager')
                self.newManager(name, f'C:\\Users\{getpass.getuser()}\AppData\Roaming\.cookies_pw_manager')
        self.refresh()

    def generator(self):
        self.add_pw.setText(pm.manager.generator(self.pw_gen_len.value()))
        self.refresh()

    def refresh(self):
        index = self.combobox_pw.currentIndex()
        try:
            self.masterPw_correct = self.manager.checkmasterPW(self.masterPW.text())
        except KeyError:
            pass
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
        self.combobox_pw.setCurrentIndex(index)

    def change_master_pw(self):
        if  (not self.masterPw_correct):
            reply = QMessageBox()
            reply.setText('Das Masterpasswort muss erst validiert werden')
            reply.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply.exec()
            return
        passwords = []
        for index in self.keys:
            if index == 'masterPassword':
                continue
            print(index)
            passwords.append((index, self.manager.read_password(index, copy = False)))
        new_pw, ok = QInputDialog.getText(self, 'Passwort', 'Bitte geb das neue Passwort ein:', QLineEdit.EchoMode.Password)
        if not ok:
            return
        self.manager.masterPassword_setter(new_pw)
        self.masterPW.setText(new_pw)
        self.manager.data= {'masterPassword':hashlib.sha512((self.manager.masterPassword).encode('ascii')).hexdigest()}
        for index in passwords:
            self.manager.add_password(index[0],index[1])
        self.refresh()
        self.manager.save()



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
        fileName = fd.getOpenFileName(self,'Open', f'C:\\Users\{getpass.getuser()}\Desktop', '(*.json)')
        self.filePath.setText(fileName[0])
        self.refresh()

    def newManager(self, text = False, filepath = None):
        try:
            if self.masterPW.text() == '':
                new_pw, ok = QInputDialog.getText(self, 'Passwort', 'Bitte geb das Masterpasswort ein:', QLineEdit.EchoMode.Password)
                if not ok:
                    return
                self.masterPW.setText(new_pw)
            new_pw_2, ok = QInputDialog.getText(self, 'Passwort', 'Bitte geb das Masterpasswort nochmal zur bestätigung ein ein:', QLineEdit.EchoMode.Password)
            if not ok:
                return
            if not self.masterPW.text() == new_pw_2:
                reply = QMessageBox()
                reply.setText('Die Passwörter stimmen nicht überein')
                reply.setStandardButtons(QMessageBox.StandardButton.Ok)
                reply.exec()
                return
            if text == False:
                text, ok = QInputDialog.getText(self, 'Dateiname', 'Bitte geb einen Dateinamen ein:')
                if not ok:
                    return

            fd = QFileDialog()
            if filepath == None:
                filepath = fd.getExistingDirectory(self,'Open', f'C:\\Users\{getpass.getuser()}\Desktop')
            if filepath == '':
                reply = QMessageBox()
                reply.setText('Kein Zielpfad ausgewählt')
                reply.setStandardButtons(QMessageBox.StandardButton.Ok)
                reply.exec()
                return
            self.manager.file = filepath.replace('/', chr(92)) + chr(92) + text + '.json'
            reply = QMessageBox()
            reply.setText('Bestehende Dateien werden überschrieben\nDies kann nicht rückgängig gemacht werden')
            reply.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            x = reply.exec()
            if(x == QMessageBox.StandardButton.Yes):
                self.manager.masterPassword_setter(self.masterPW.text())
                self.filePath.setText(self.manager.file)
                try:
                    self.manager.create_new_manager()
                except PermissionError:
                    reply = QMessageBox()
                    reply.setText('Permission Denied')
                    reply.setStandardButtons(QMessageBox.StandardButton.Ok)
                    reply.exec()
                    return
                self.refresh()
        except AttributeError:
            reply = QMessageBox()
            reply.setText('Es muss erst ein Dateipfad ausgewählt werden')
            reply.setStandardButtons(QMessageBox.StandardButton.Ok )
            x = reply.exec()
            self.refresh()
