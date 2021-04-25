import globals
from hotkeys import start_hotkey_listener, any_hotkeys_set
from gui import Root, MainWindow, raise_above_all

#TODO
#using quickload hotkey completely breaks the hotkeys
#raise_above_all should select the window
#change hotkeys to be set by keyboard presses

def main():
    globals.init()

    root = Root()
    root.wm_title("BloonsTD6 Save Scummer")
    root.geometry("341x312")
    mainWindow = MainWindow(root)
    raise_above_all(root)

    if any_hotkeys_set():
        start_hotkey_listener(mainWindow)

    root.mainloop()

if __name__ == "__main__":
    main()
