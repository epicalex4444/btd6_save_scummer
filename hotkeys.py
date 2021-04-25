import pynput
import globals
from functions import create_save, load_save

currentListener = None

def save(mainWindow):
    mainWindow.save_hotkey()
    print('save')

def load(mainWindow):
    mainWindow.load_hotkey()
    print('load')

def quicksave():
    create_save('quicksave')
    print('quicksave')

def quickload():
    load_save('quicksave')
    print('quickload')

def any_hotkeys_set():
    return not (globals.SAVE_HOTKEY == None and globals.LOAD_HOTKEY == None and globals.QUICKSAVE_HOTKEY == None and globals.QUICKLOAD_HOTKEY == None)

#get hotkeys and starts listener in a non blocking way, stops existing listener if any
def start_hotkey_listener(mainWindow):
    global currentListener
    if currentListener != None:
        currentListener.stop()

    hotkeys = dict()
    if globals.SAVE_HOTKEY != None:
        hotkeys[globals.SAVE_HOTKEY] = lambda: save(mainWindow)
    if globals.LOAD_HOTKEY != None:
        hotkeys[globals.LOAD_HOTKEY] = lambda: load(mainWindow)
    if globals.QUICKSAVE_HOTKEY != None:
        hotkeys[globals.QUICKSAVE_HOTKEY] = quicksave
    if globals.QUICKLOAD_HOTKEY != None:
        hotkeys[globals.QUICKLOAD_HOTKEY] = quickload

    currentListener = pynput.keyboard.GlobalHotKeys(hotkeys)
    currentListener.start()
