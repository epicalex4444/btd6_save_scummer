import os
import shutil
import psutil
import subprocess
import json
import globals
from exceptions import *

def list_save_names():
    check_local_save_folder()
    saves = []
    for folder in os.scandir(globals.LOCAL_SAVE_DIR):
        if (folder.is_dir() and folder.name != 'quicksave'):
            saves.append(folder.name)
    return saves

def close_btd6():
    for process in psutil.process_iter():
        if process.name() == 'BloonsTD6.exe':
            os.kill(process.pid, 9)

    #waits until btd6 is closed before exiting function
    #potentially this could become an infite loop
    btd6Open = True
    while btd6Open:
        btd6Open = False
        for process in psutil.process_iter():
            if process.name() == 'BloonsTD6.exe':
                btd6Open = True

def open_btd6():
    if not btd6_exe_valid():
        raise IncorrectBtd6ExeDir
    subprocess.Popen(args=[], executable=globals.BTD6_EXE)

def export_setings():
    settings = {
        'BTD6_SAVE_DIR': globals.BTD6_SAVE_DIR,
        'BTD6_EXE': globals.BTD6_EXE,
        'SAVE_HOTKEY': globals.SAVE_HOTKEY,
        'LOAD_HOTKEY': globals.LOAD_HOTKEY,
        'QUICKSAVE_HOTKEY': globals.QUICKSAVE_HOTKEY,
        'QUICKLOAD_HOTKEY': globals.QUICKLOAD_HOTKEY
    }

    try:
        file = open(globals.SETTINGS_FILE, 'w')
    except IOError:
        file = open(globals.SETTINGS_FILE, 'x')
    finally:
        json.dump(settings, file, indent=4)
        file.close()

def create_save(saveName:str):
    if not btd6_save_dir_valid():
        raise IncorrectBtd6SaveDir
    
    check_local_save_folder()

    if globals.BTD6_SAVE_DIR == None:
        raise InvalidSettingsError

    localSaveDir = globals.LOCAL_SAVE_DIR + saveName + '\\'
    if not os.path.isdir(localSaveDir):
        os.mkdir(localSaveDir)
    elif not (saveName == 'quicksave' or saveName == 'backup'):
        raise SaveExistsError

    shutil.copy(globals.BTD6_SAVE_DIR + 'Profile.Save', localSaveDir)
    shutil.copy(globals.BTD6_SAVE_DIR + 'Profile.bak', localSaveDir)

def delete_save(saveName:str):
    check_local_save_folder()
    if not os.path.isdir(globals.LOCAL_SAVE_DIR + saveName):
        raise SaveNotFoundError
    shutil.rmtree(globals.LOCAL_SAVE_DIR + saveName)

def load_save(saveName:str):
    if not btd6_save_dir_valid():
        raise IncorrectBtd6SaveDir
    
    check_local_save_folder()

    if not save_valid(saveName):
        raise SaveMissingData

    if globals.BTD6_SAVE_DIR == None or globals.BTD6_EXE == None:
        raise InvalidSettingsError

    localSaveDir = globals.LOCAL_SAVE_DIR + saveName + '\\'
    if not os.path.isdir(localSaveDir):
        raise SaveNotFoundError

    close_btd6()

    shutil.copy(localSaveDir + 'Profile.Save', globals.BTD6_SAVE_DIR)
    shutil.copy(localSaveDir + 'Profile.bak', globals.BTD6_SAVE_DIR)

    open_btd6()

#returns None if there is no settings file
def read_settings():
    if not os.path.isfile(globals.SETTINGS_FILE):
        return None
    file = open(globals.SETTINGS_FILE, 'r')
    settings = json.load(file)
    file.close()
    return settings

#gets the btd6_save_scummer directory, assumes this file is in that directory
def get_directory():
    return os.path.dirname(os.path.realpath(__file__)) + '\\'

#makes save folder if it doesn't exist make one
def check_local_save_folder():
    if not os.path.isdir(globals.LOCAL_SAVE_DIR):
        os.mkdir(globals.LOCAL_SAVE_DIR)

def btd6_exe_valid():
    try:
        return os.path.isfile(globals.BTD6_EXE) and globals.BTD6_EXE.endswith('\\BloonsTD6.exe')
    except:
        return False

def btd6_save_dir_valid():
    try:
        return os.path.isfile(globals.BTD6_SAVE_DIR + 'Profile.Save')
    except:
        return False

def save_valid(saveName:str):
    localSaveDir = globals.LOCAL_SAVE_DIR + saveName + '\\'
    try:
        save = os.path.isfile(localSaveDir + 'Profile.Save')
        bak = os.path.isfile(localSaveDir + 'Profile.bak')
        return save and bak
    except:
        return False
