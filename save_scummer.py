import globals
from hotkeys import start_hotkey_listener, any_hotkeys_set, check_hotkeys_valid
from gui import Root, MainWindow

def main():
    globals.init()

    root = Root()
    mainWindow = MainWindow(root)

    check_hotkeys_valid()
    if any_hotkeys_set():
        start_hotkey_listener(mainWindow)

    root.mainloop()

if __name__ == "__main__":
    main()
