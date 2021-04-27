import pynput
import globals
from functions import create_save, load_save
import threading

def any_hotkeys_set():
    return not (globals.SAVE_HOTKEY == None and globals.LOAD_HOTKEY == None and globals.QUICKSAVE_HOTKEY == None and globals.QUICKLOAD_HOTKEY == None)

def get_hotkeys(mainWindow):
    hotkeys = dict()
    if globals.SAVE_HOTKEY != None:
        hotkeys[globals.SAVE_HOTKEY] = mainWindow.save_hotkey
    if globals.LOAD_HOTKEY != None:
        hotkeys[globals.LOAD_HOTKEY] = mainWindow.load_hotkey
    if globals.QUICKSAVE_HOTKEY != None:
        hotkeys[globals.QUICKSAVE_HOTKEY] = lambda: create_save('quicksave')
    if globals.QUICKLOAD_HOTKEY != None:
        hotkeys[globals.QUICKLOAD_HOTKEY] = lambda: load_save('quicksave')
    return hotkeys

#automatically starts in a non blocking way and handles hotkey calls in a non blocking way
class SmartHotkeyListener(pynput.keyboard.Listener):
    def __init__(self, hotkeys:dict):
        super().__init__(on_press=self.on_press, on_release=self.on_release)
        self.hotkeys = [pynput.keyboard.HotKey.parse(hotkey) for hotkey in hotkeys]
        self.functions = [hotkeys[hotkey] for hotkey in hotkeys]
        self.currentKeys = set()
        self.executeThread = None
        self.lock = threading.Lock()
        self.start()

    #if hotkeys share a same key there will be a priority in which one is activated in this system
    #as only one hotkey can be activated from a button press, hotkeys are also considered unordered
    #using a hotkey when one is still being active will cause it not to activate
    def on_press(self, key):
        key = self.canonical(key)
        self.currentKeys.add(key)
        for i, hotkey in enumerate(self.hotkeys):
            if not key in hotkey:
                continue
            if self.hotkey_active(hotkey):
                if not self.lock.locked():
                    self.close_thread() #if the lock has been released we know the thread is ready to exit
                    self.executeThread = threading.Thread(target=self.execute_function(self.functions[i]))
                    self.executeThread.start()
                return

    def on_release(self, key):
        key = self.canonical(key)
        if key in self.currentKeys:
            self.currentKeys.remove()

    def hotkey_active(self, hotkey):
        hotkeyActive = True
        for key in hotkey:
            if not key in self.currentKeys:
                hotkeyActive = False
        return hotkeyActive

    def execute_function(self, function):
        self.lock.acquire()
        function()
        self.lock.release()

    #this operation involves waiting for a thread to finish, which can be slow
    def close_thread(self):
        if self.executeThread != None:
            self.executeThread.join()

    def stop(self):
        self.close_thread()
        super().stop()

#starts/restarts hotkey handling
def start_hotkey_listener(mainWindow):
    if globals.LISTENER != None:
        globals.LISTENER.stop()
    globals.LISTENER = SmartHotkeyListener(get_hotkeys(mainWindow))
