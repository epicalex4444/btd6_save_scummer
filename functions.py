import os
import shutil
import psutil
import subprocess
import json
import globals
from exceptions import SaveNotFoundError, SaveExistsError, InvalidSettingsError

def list_save_names():
    check_save_folder()
    saveNames = []
    files = os.listdir(globals.LOCAL_SAVE_DIR)
    for fileName in files:
        if fileName.endswith('.Save') and fileName != 'quicksave.Save':
            saveNames.append(file[:-5])
    return saveNames

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
    check_save_folder()
    if globals.BTD6_SAVE_DIR == None:
        raise InvalidSettingsError
    if os.path.isfile(globals.LOCAL_SAVE_DIR + saveName + '.Save') and saveName != 'quicksave':
        raise SaveExistsError
    
    src = globals.BTD6_SAVE_DIR + 'Profile.Save'
    dst = globals.LOCAL_SAVE_DIR
    shutil.copy(src, dst)

    src = globals.LOCAL_SAVE_DIR + 'Profile.Save'
    dst = globals.LOCAL_SAVE_DIR + saveName + '.Save'
    shutil.move(src, dst)

def delete_save(saveName:str):
    check_save_folder()
    if not os.path.isfile(globals.LOCAL_SAVE_DIR + saveName + '.Save'):
        raise SaveNotFoundError
    os.remove(globals.LOCAL_SAVE_DIR + saveName + '.Save')

def load_save(saveName:str):
    check_save_folder()
    if globals.BTD6_SAVE_DIR == None or globals.BTD6_EXE == None:
        raise InvalidSettingsError
    if not os.path.isfile(globals.LOCAL_SAVE_DIR + saveName + '.Save'):
        raise SaveNotFoundError

    close_btd6()

    src = globals.LOCAL_SAVE_DIR + saveName + '.Save'
    dst = globals.BTD6_SAVE_DIR
    shutil.copy(src, dst)

    src = globals.BTD6_SAVE_DIR + saveName + '.Save'
    dst = globals.BTD6_SAVE_DIR + 'Profile.Save'
    shutil.move(src, dst)

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

#makes save folder if it doesn't exist
def check_save_folder():
    if not os.path.isdir(globals.LOCAL_SAVE_DIR):
        os.mkdir(globals.LOCAL_SAVE_DIR)
