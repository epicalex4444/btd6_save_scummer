import pynput
import globals
from functions import create_save, load_save
import threading
import queue

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
        self.queue = queue.PriorityQueue()
        self.sigStop = (0, -1) #breaks executors while loop when added to the queue
        self.executor = threading.Thread(target=lambda: self.executor_callback(self.functions))
        self.executor.start()
        self.start()

    #if hotkeys share a same key there will be a priority in which one is activated in this system
    #as only one hotkey can be activated from a button press, hotkeys are also considered unordered
    def on_press(self, key):
        key = self.canonical(key)
        self.currentKeys.add(key)
        for i, hotkey in enumerate(self.hotkeys):
            if not key in hotkey:
                continue
            if self.hotkey_active(hotkey):
                self.queue.put_nowait((10, i))
                return

    def on_release(self, key):
        self.currentKeys.remove(self.canonical(key))

    def hotkey_active(self, hotkey):
        hotkeyActive = True
        for key in hotkey:
            if not key in self.currentKeys:
                hotkeyActive = False
        return hotkeyActive

    def executor_callback(self, functions:tuple):
        while True:
            if self.queue.empty():
                continue
            msg = self.queue.get_nowait()
            if msg[1] == -1:
                return
            functions[msg[1]]()
            self.queue.task_done()

    def stop(self):
        self.queue.put_nowait(self.sigStop)
        self.executor.join()
        super().stop()

#starts/restarts hotkey handling
def start_hotkey_listener(mainWindow):
    if globals.LISTENER != None:
        globals.LISTENER.stop()
    globals.LISTENER = SmartHotkeyListener(get_hotkeys(mainWindow))
