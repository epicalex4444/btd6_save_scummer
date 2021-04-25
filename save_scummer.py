import os
import shutil
import psutil
import subprocess
import tkinter as tk
from tkinter import messagebox
import json

#root class used to override the default error handling of tkinter
class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def report_callback_exception(self, exc, val, tb):
        messagebox.showerror('Error', str(val))

#custom exceptions
class SaveNotFoundError(Exception):
    def __init__(self, message="save doesn't exist"):
        self.message = message
        super().__init__(self.message)

class SaveExistsError(Exception):
    def __init__(self, message="save already exists"):
        self.message = message
        super().__init__(self.message)

class InvalidSettingsError(Exception):
    def __init__(self, message='BTD6 Save Directory or BTD6 Exe Directory are not set'):
        self.message = message
        super().__init__(self.message)

#contains properties for a save
class Save():
    def __init__(self, name:str, label:tk.Label, loadButton:tk.Button, deleteButton:tk.Button):
        self.name = name
        self.label = label
        self.loadButton = loadButton
        self.deleteButton = deleteButton

#model for the app window, handles all buttons labels and such
class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack(fill=tk.BOTH, expand=1)
        self.column0Width = 30
        self.column1Width = 4
        self.column2Width = 7
        self.inputText = tk.Text(self, height=1, width=self.column0Width)
        saveButton = tk.Button(self, text='Save', command=self.create_save, width=self.column1Width)
        settingsButton = tk.Button(self, text='Settings', command=self.create_settings, width=self.column2Width)
        self.inputText.grid(row=0, column=0)
        saveButton.grid(row=0, column=1)
        settingsButton.grid(row=0, column=2)
        self.saves = []
        self.init_saves()
        self.place_saves()
        if BTD6_SAVE_DIR == None or BTD6_EXE == None:
            tk.messagebox.showwarning('Missing Settings', 'BTD6 Save Directory or BTD6 Exe Directory are not set, you will need to go to settings to use the save and load features of this program')

    #makes a list of Saves() from existing files in the dir
    def init_saves(self):
        saveNames = list_saves()

        for saveName in saveNames:
            self.add_save(saveName)

    #places the label and buttons for all the saves, moves them if already placed
    def place_saves(self):
        for i, save in enumerate(self.saves):
            save.label.grid(row=i + 1, column=0)
            save.loadButton.grid(row=i + 1, column=1)
            save.deleteButton.grid(row=i + 1, column=2)

    #appends save to save list and window
    def add_save(self, saveName:str):
        label = tk.Label(self, text=saveName, width=self.column0Width)
        loadButton = tk.Button(self, text='Load', command=lambda: self.load_save(saveName), width=self.column1Width)
        deleteButton = tk.Button(self, text='Delete', command=lambda: self.delete_save(saveName), width=self.column2Width)
        self.saves.append(Save(saveName, label, loadButton, deleteButton))
        self.place_saves()

    #removes save from save list and window
    def remove_save(self, saveName:str):
        for i, save in enumerate(self.saves):
            if save.name == saveName:
                save.label.destroy()
                save.loadButton.destroy()
                save.deleteButton.destroy()
                self.saves.pop(i)
                self.place_saves()
                return
        
    #adds new save to the window and in the saves list, gets name from input box
    def create_save(self):
        if BTD6_SAVE_DIR == None:
            raise InvalidSettingsError

        saveName = self.inputText.get('1.0', 'end-1c')

        if os.path.isfile(LOCAL_SAVE_DIR + saveName + '.Save'):
            raise SaveExistsError
    
        #copy Profile.Save to LOCAL_SAVE_DIR
        src = BTD6_SAVE_DIR + BTD6_SAVE_NAME
        dst = LOCAL_SAVE_DIR
        shutil.copy(src, dst)

        #rename Profile.Save to saveName.Save
        src = LOCAL_SAVE_DIR + BTD6_SAVE_NAME
        dst = LOCAL_SAVE_DIR + saveName + '.Save'
        shutil.move(src, dst)

        self.add_save(saveName)

    #removes save from window and saves list
    def delete_save(self, saveName:str):
        answer = messagebox.askyesno('Delete Save Conformation', 'Are you sure you want to delete {0}?'.format(saveName))
        if answer == False:
            return

        if not os.path.isfile(LOCAL_SAVE_DIR + saveName + '.Save'):
            self.remove_save(saveName) #removes faulty save entry
            raise SaveNotFoundError

        os.remove(LOCAL_SAVE_DIR + saveName + '.Save')
        self.remove_save(saveName)

    #reopens btd6 with the chosen save
    def load_save(self, saveName:str):
        if BTD6_SAVE_DIR == None or BTD6_EXE == None:
            raise InvalidSettingsError

        if not os.path.isfile(LOCAL_SAVE_DIR + saveName + '.Save'):
            self.remove_save(saveName) #removes faulty save entry
            raise SaveNotFoundError

        #btd6 has to be opened and closed to load a save
        close_btd6()

        #copy saveName.Save to BTD6_SAVE_DIR
        src = LOCAL_SAVE_DIR + saveName + '.Save'
        dst = BTD6_SAVE_DIR
        shutil.copy(src, dst)

        #rename saveName.Save to Profile.Save, overriding existing Profile.Save
        src = BTD6_SAVE_DIR + saveName + '.Save'
        dst = BTD6_SAVE_DIR + BTD6_SAVE_NAME
        shutil.move(src, dst)

        open_btd6()

    #opens a settings subwindow
    def create_settings(self):
        Settings(self.root)

#Settings Sub Menu for the MainWindow
class Settings(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title('Settings for BloonsTD6 Save Scummer')
        self.geometry('382x78')

        exeDirButtonLabel = tk.Label(self, text='BTD6 Exe Directory')
        self.exeDirButtonText = tk.Text(self, height=1, width=30)
        exeDirButton = tk.Button(self, text='Set', command=lambda: set_btd6_exe(self))

        saveDirButtonLabel = tk.Label(self, text='BTD6 Save Directory')
        self.saveDirButtonText = tk.Text(self, height=1, width=30)
        saveDirButton = tk.Button(self, text='Set', command=lambda: set_btd6_save_dir(self))

        helpButton = tk.Button(self, text="Help Me, I Don't Where Those Directories Are", command=lambda: help_msg(self))

        exeDirButtonLabel.grid(row=0, column=0)
        self.exeDirButtonText.grid(row=0, column=1)
        exeDirButton.grid(row=0, column=2)

        saveDirButtonLabel.grid(row=1, column=0)
        self.saveDirButtonText.grid(row=1, column=1)
        saveDirButton.grid(row=1, column=2)

        helpButton.grid(row=2, column=0, columnspan=3)

        def set_btd6_exe(self):
            textInput = self.exeDirButtonText.get('1.0', 'end-1c')
            if not textInput.endswith('\\'):
                textInput += '\\'
            global BTD6_EXE
            BTD6_EXE = textInput + 'BloonsTD6.exe'
            export_setings()

        def set_btd6_save_dir(self):
            textInput = self.saveDirButtonText.get('1.0', 'end-1c')
            if not textInput.endswith('\\'):
                textInput += '\\'
            global BTD6_SAVE_DIR
            BTD6_SAVE_DIR = textInput
            export_setings()

        def help_msg(self):
            HelpMessage(self)

#Help Message sub window for Settings Window
class HelpMessage(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title('Help Message')
        helpText = tk.Label(self, text=SETTING_HELP_MSG)
        helpText.pack()

#gets a list of save names from the LOCAL_SAVE_DIR
def list_saves():
    saves = []
    files = os.listdir(LOCAL_SAVE_DIR)
    for file in files:
        if file.endswith('.Save'):
            saves.append(file[:-5])
    return saves

#closes all instances of BloonsTD6.exe
def close_btd6():
    for process in psutil.process_iter():
        if process.name() == 'BloonsTD6.exe':
            os.kill(process.pid, 9)

    btd6Open = True
    while btd6Open:
        btd6Open = False
        for process in psutil.process_iter():
            if process.name() == 'BloonsTD6.exe':
                btd6Open = True

#opens an instance of BloonsTD6.exe
def open_btd6():
    subprocess.Popen(args=[], executable=BTD6_EXE)

#exports the setting into a json file, so variables can be saved when the program is closed
def export_setings():
    settings = {
        'BTD6_SAVE_DIR': BTD6_SAVE_DIR,
        'BTD6_EXE': BTD6_EXE
    }

    try:
        file = open(SETTINGS_FILE, 'w')
    except IOError:
        file = open(SETTINGS_FILE, 'x')
    finally:
        json.dump(settings, file, indent=4)
        file.close()

#entry point, with a guard so file is only ran if it is the main
if __name__ == "__main__":
    BTD6_SAVE_NAME = 'Profile.Save'
    FILE_DIR = os.path.dirname(os.path.realpath(__file__)) + '\\'
    LOCAL_SAVE_DIR = FILE_DIR + 'saves\\'
    SETTINGS_FILE = FILE_DIR + 'settings.json'
    SETTING_HELP_MSG = '''BTD6 Exe Directory is the location of the BloonsTD6.exe, it is generelly
    C:\\Program Files (x86)\\Steam\\steamapps\\common\\BloonsTD6\\.
    You can get to this address through steam by browsing local files.

    BTD6 Save Directory is the location that BTD6 puts save data there will be a file
    called Profile.Save in the directory. Generelly you should go to
    C:\\Program Files (x86)\\Steam\\userdata\\, from there the number after userdata
    indicates which steam account, you can find your steam id at
    https://steamidfinder.com/. The number after that indicates the game, 
    btd6 is 960090, after that the folders should be linear leading to Profile.Save

    once you have found these folder you can right click the address at the 
    top of file explorer and copy as text and paste in into the input boxes'''

    if not os.path.isdir(LOCAL_SAVE_DIR):
        os.mkdir(LOCAL_SAVE_DIR)

    BTD6_SAVE_DIR = None
    BTD6_EXE = None
    if os.path.isfile(SETTINGS_FILE):
        file = open(SETTINGS_FILE, 'r')
        settings = json.load(file)
        file.close()
        BTD6_SAVE_DIR = settings['BTD6_SAVE_DIR']
        BTD6_EXE = settings['BTD6_EXE']

    root = Root()
    root.wm_title("BloonsTD6 Save Scummer")
    root.geometry("341x312")
    app = MainWindow(root)
    root.mainloop()
