import pynput
from hotkeys import get_vk

allKeys = []

#adds keys pressed into allKeys, and closes itself once every key is released
class HotkeySetter(pynput.keyboard.Listener):
    def __init__(self):
        super().__init__(on_press=self.on_press, on_release=self.on_release)
        self.currentKeys = set()
    
    def on_press(self, key):
        key = get_vk(key)
        self.currentKeys.add(key)
        if not key in allKeys:
            allKeys.append(key)

    def on_release(self, key):
        key = get_vk(key)
        if key in self.currentKeys:
            self.currentKeys.remove(key)
        if self.currentKeys == set():
            self.stop()

def get_new_hotkey():
    global allKeys
    allKeys = []
    with HotkeySetter() as listener:
        listener.join()
    return tuple(allKeys)

#couldn't find any library to do this shit for me
#many buttons are missing but it's unlikely people will use those buttons anyway
def hotkey_to_string(hotkey):
    if hotkey == ():
        return 'Hotkey Not Set'

    vk_names = [
    'lbutton',
    'rbutton',
    'cancel',
    'mbutton',
    'xbutton1',
    'xbutton2',
    'unknown',
    'backspace',
    'tab',
    'unknown',
    'unknown',
    'unknown',
    'enter',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'capslock',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'esc',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'space',
    'pgup',
    'pgdown',
    'end',
    'home',
    'left',
    'up',
    'right',
    'down',
    'unknown',
    'unknown',
    'unknown',
    'prtsc',
    'insert',
    'delete',
    'unknown',
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z',
    'lwin',
    'rwin',
    'unknown',
    'unknown',
    'unknown',
    'numpad0',
    'numpad1',
    'numpad2',
    'numpad3',
    'numpad4',
    'numpad5',
    'numpad6',
    'numpad7',
    'numpad8',
    'numpad9',
    'numpad*',
    'numpad+',
    'unknown',
    'numpad-',
    'numpad.',
    'numpad/',
    'f1',
    'f2',
    'f3',
    'f4',
    'f5',
    'f6',
    'f7',
    'f8',
    'f9',
    'f10',
    'f11',
    'f12',
    'f13',
    'f14',
    'f15',
    'f16',
    'f17',
    'f18',
    'f19',
    'f20',
    'f21',
    'f22',
    'f23',
    'f24',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'numlock',
    'scrolllock',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'lshift',
    'rshift',
    'lctrl',
    'rctrl',
    'lalt',
    'ralt',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    ';',
    '=',
    ',',
    '-',
    '.',
    '/',
    '`',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    '[',
    '\\',
    ']',
    "'",
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown',
    'unknown'
    ]

    hotkeyStr = ""
    for vk in hotkey:
        hotkeyStr += vk_names[vk - 1] + ' + '
    return hotkeyStr[:-3]
