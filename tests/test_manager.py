import pytest
import random
import sys
sys.path.append("..")
import password_manager

def test_generator():
    for _ in range(128):
        x = random.randint(1, 1024)
        assert len(password_manager.manager.generator(x)) == x
        assert not password_manager.manager.generator(x) == password_manager.manager.generator(x)

def test_start():
    pass
def test_cheackmasterPW():
    pass

def test_initialisiere():
    pass

def test_add_password():
    pass

def test_save_read():
    pass

def create_new_manager():
    pass
