from functions import get_directory, read_settings

def init():
    global LOCAL_SAVE_DIR
    global SETTINGS_FILE
    global BTD6_SAVE_DIR
    global BTD6_EXE
    global HELP_MSG

    fileDir = get_directory()
    LOCAL_SAVE_DIR = fileDir + 'saves\\'
    SETTINGS_FILE = fileDir + 'settings.json'
    settings = read_settings()
    BTD6_SAVE_DIR = None
    BTD6_EXE = None
    if settings != None:
        BTD6_SAVE_DIR = settings['BTD6_SAVE_DIR']
        BTD6_EXE = settings['BTD6_EXE']
    HELP_MSG = '''BTD6 Exe Directory is the location of the BloonsTD6.exe, it is generelly
    C:\\Program Files (x86)\\Steam\\steamapps\\common\\BloonsTD6\\.
    You can get to this address through steam by browsing local files.

    BTD6 Save Directory is the location that BTD6 puts save data there will be a file
    called Profile.Save in the directory. Generelly you should go to
    C:\\Program Files (x86)\\Steam\\userdata\\, from there the number after userdata
    indicates which steam account, you can find your steam id at
    https://steamidfinder.com/. The number after that indicates the game, 
    btd6 is 960090, after that the folders should be linear leading to Profile.Save.

    once you have found these folder you can right click the address at the 
    top of file explorer and copy as text and paste in into the input boxes.'''
