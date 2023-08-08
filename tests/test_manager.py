import random

import os
import sys

import clipboard
import pytest
import pytest

sys.path.append(os.getcwd())
from modules import manager
number_of_trials = 128


def test_generator():
    global number_of_trials
    for _ in range(number_of_trials):
        x = random.randint(1, 1024)
        assert len(manager.generator(x)) == x
        assert not manager.generator(x) == manager.generator(x)
    with pytest.raises(ValueError, match='x has to be a positive integer'):
        manager.generator(-42)

def test_start():
    m = manager()
    m.start("Random_String", "Random_Name")
    assert m.data == {}
    assert len(m.masterPassword) == 32
    assert len(m.salt) == 32
    assert m.file == "Random_Name"

def test_cheackmasterPW():
    m = manager()
    m.start("Random_String", "tests/for_testing.json")
    assert m.checkmasterPW("Random_String")
    m = manager()
    m.start("Random_String", "tests/for_testing.json")
    assert not m.checkmasterPW(None)
    m.start(None, "tests/for_testing.json")
    assert not m.checkmasterPW("Random_String")
    m.start("Random_String", None)
    assert not m.checkmasterPW("Random_String")

    for _ in range(number_of_trials):
        x = random.randint(1, 1024)
        random_pw = manager.generator(x)
        another_random_pw = manager.generator(x)
        m.masterPassword_setter(random_pw)
        assert not m.checkmasterPW(another_random_pw)

def test_add_password():
    global number_of_trials
    file = 'tests/only_temporary.json'
    for _ in range(number_of_trials):
        print(_)
        x = random.randint(1, 32)
        m = manager()
        m.start('', file)
        random_master_pw = manager.generator(x)
        m.masterPassword_setter(random_master_pw)
        m.create_new_manager()
        pw_list = []
        name_list = []
        for _ in range(number_of_trials):
            x = random.randint(1, 1024)
            y = random.randint(1, 32)
            random_pw = manager.generator(x)
            random_name = manager.generator(y)
            if random_name in name_list:
                continue
            m.add_password(random_name, random_pw)
            pw_list.append(random_pw)
            name_list.append(random_name)
            assert len(m.read_password(random_name)) == len(random_pw)
            assert clipboard.paste() == random_pw
            assert m.read_password(random_name, copy=False) == random_pw
        assert len(name_list) == len(pw_list)

        for (name, pw) in zip(name_list, pw_list):
            assert m.read_password(name, copy=False) == pw
        m.save()
        del m
        m = manager()
        m.start('', file)
        m.masterPassword_setter(random_master_pw)
        for (name, pw) in zip(name_list, pw_list):
            assert m.read_password(name, copy=False) == pw
        os.remove(file)



def test_create_new_manager():
    global number_of_trials
    file = 'tests/only_temporary.json'
    m = manager()
    m.start('', file)
    for _ in range(number_of_trials):
        x = random.randint(1, 32)
        random_master_pw = manager.generator(x)
        m.masterPassword_setter(random_master_pw)
        m.create_new_manager()
        assert m.checkmasterPW(random_master_pw)
    os.remove(file)

