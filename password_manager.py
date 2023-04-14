import random
import json
import hashlib
import sys
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import clipboard
class manager(object):
    iv = b'idhnclx1734bs8av'

    def __init__(self):
        self.salt = ''
        self.masterPassword = ''
        self.start('', '')

    def masterPassword_setter(self, value:str)->None:
        r =  random.Random(value)
        self.salt = ''
        for i in range(32):
            self.salt += (chr((int(r.random()*(127-33))+33)))
        self.masterPassword = value + self.salt[len(value):]

    def start(self, masterPassword:str, file:str)->None:
        self.masterPassword_setter(masterPassword)
        self.file = file
        self.data = {}
        self.initialisiere()

    def checkmasterPW(self, pw:str)->bool:
        r =  random.Random(pw)
        salt = ''
        for i in range(32):
            salt += (chr((int(r.random()*(127-33))+33)))
        if(hashlib.sha512((pw + salt[len(pw):]).encode('ascii')).hexdigest() == self.data['masterPassword']):
            self.masterPassword_setter(pw+salt[len(pw):])
            return True
        return False

    def initialisiere(self)->None:
        try:
            with open(self.file,'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            pass
        except NameError:
            pass

    def add_password(self, password_site:str, password:str) -> None:
        cipher = AES.new(key = self.masterPassword.encode(), mode = AES.MODE_CFB, iv = manager.iv)
        ct_bytes = cipher.encrypt(password.encode())
        self.data[password_site] = b64encode(ct_bytes).decode('ascii')
        self.save()

    def save(self) -> None:
        with open(self.file, 'w') as f:
            json.dump(self.data,f, indent = 4)

    def read_password(self, password_site:str, copy = True)-> str:
        cipher = AES.new(key = self.masterPassword.encode(), mode = AES.MODE_CFB, iv = manager.iv)
        x = (cipher.decrypt(b64decode(self.data[password_site])))
        del cipher
        if copy:
            clipboard.copy(x.decode('ascii'))
        return x.decode('ascii')

    def create_new_manager(self) -> None:
        self.data= {'masterPassword':hashlib.sha512((self.masterPassword).encode('ascii')).hexdigest()}
        with open(self.file, 'w') as f:
            json.dump(self.data,f, indent = 4)

    @staticmethod
    def generator(x: int = 64) -> str:
        if (type(x) is not int or x <0):
            raise ValueError('x has to be a positive integer')
        return "".join(random.choices(string.printable, k=x))
