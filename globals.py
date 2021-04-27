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

    fileDir = get_directory()
    LOCAL_SAVE_DIR = fileDir + 'saves\\'
    SETTINGS_FILE = fileDir + 'settings.json'
    settings = read_settings()
    BTD6_SAVE_DIR = None
    BTD6_EXE = None
    SAVE_HOTKEY = ()
    LOAD_HOTKEY = ()
    QUICKSAVE_HOTKEY = ()
    QUICKLOAD_HOTKEY = ()
    if settings != None:
        BTD6_SAVE_DIR = settings.get('BTD6_SAVE_DIR', None)
        BTD6_EXE = settings.get('BTD6_EXE', None)
        SAVE_HOTKEY = settings.get('SAVE_HOTKEY', ())
        LOAD_HOTKEY = settings.get('LOAD_HOTKEY', ())
        QUICKSAVE_HOTKEY = settings.get('QUICKSAVE_HOTKEY', ())
        QUICKLOAD_HOTKEY = settings.get('QUICKLOAD_HOTKEY', ())

    if SAVE_HOTKEY != ():
        SAVE_HOTKEY = tuple(SAVE_HOTKEY)
    if LOAD_HOTKEY != ():
        LOAD_HOTKEY = tuple(LOAD_HOTKEY)
    if QUICKSAVE_HOTKEY != ():
        QUICKSAVE_HOTKEY = tuple(QUICKSAVE_HOTKEY)
    if QUICKLOAD_HOTKEY != ():
        QUICKLOAD_HOTKEY = tuple(QUICKLOAD_HOTKEY)
