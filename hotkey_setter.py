import pynput

allKeys = []

class HotkeySetter(pynput.keyboard.Listener):
    def __init__(self):
        super().__init__(on_press=self.on_press, on_release=self.on_release)
        self.currentKeys = set()
    
    def on_press(self, key):
        key = self.canonical(key)
        self.currentKeys.add(key)
        if not key in allKeys:
            allKeys.append(key)

    def on_release(self, key):
        key = self.canonical(key)
        if key in self.currentKeys:
            self.currentKeys.remove(key)
        if self.currentKeys == set():
            self.stop()

def get_hotkey():
    with HotkeySetter() as listener:
        listener.join()
    return allKeys
