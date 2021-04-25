import globals
from gui import Root, MainWindow
from functions import read_settings, get_directory
 
def main():
    globals.init()
    root = Root()
    root.wm_title("BloonsTD6 Save Scummer")
    root.geometry("341x312")
    mainWindow = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
