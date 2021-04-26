from functions import get_directory, read_settings

def init():
    global LOCAL_SAVE_DIR
    global SETTINGS_FILE
    global BTD6_SAVE_DIR
    global BTD6_EXE
    global SAVE_HOTKEY
    global LOAD_HOTKEY
    global QUICKSAVE_HOTKEY
    global QUICKLOAD_HOTKEY
    global LISTENER

    LISTENER = None
    fileDir = get_directory()
    LOCAL_SAVE_DIR = fileDir + 'saves\\'
    SETTINGS_FILE = fileDir + 'settings.json'
    settings = read_settings()
    BTD6_SAVE_DIR = None
    BTD6_EXE = None
    SAVE_HOTKEY = None
    LOAD_HOTKEY = None
    QUICKSAVE_HOTKEY = None
    QUICKLOAD_HOTKEY = None
    if settings != None:
        BTD6_SAVE_DIR = settings.get('BTD6_SAVE_DIR', None)
        BTD6_EXE = settings.get('BTD6_EXE', None)
        SAVE_HOTKEY = settings.get('SAVE_HOTKEY', None)
        LOAD_HOTKEY = settings.get('LOAD_HOTKEY', None)
        QUICKSAVE_HOTKEY = settings.get('QUICKSAVE_HOTKEY', None)
        QUICKLOAD_HOTKEY = settings.get('QUICKLOAD_HOTKEY', None)
