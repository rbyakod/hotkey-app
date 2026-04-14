# hotkey_daemon.py
from pynput import keyboard
from hotkey_launcher import HotkeyLauncher

CHAR_TO_HOTKEY_NAME = {
    "1": "ctrl+1",
    "2": "ctrl+2",
    "3": "ctrl+3",
    "4": "ctrl+4",
    "5": "ctrl+5",
    "6": "ctrl+6",
    "7": "ctrl+7",
    "8": "ctrl+8",
    "9": "ctrl+9",
    "0": "ctrl+0",
    "-": "ctrl+-",
    "=": "ctrl+=",
}

launcher = HotkeyLauncher()
ctrl_pressed = False


def on_press(key):
    global ctrl_pressed

    if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        ctrl_pressed = True
        return

    if not ctrl_pressed or not isinstance(key, keyboard.KeyCode):
        return

    hotkey_name = CHAR_TO_HOTKEY_NAME.get(key.char)
    if hotkey_name:
        print(f"Hotkey pressed: {hotkey_name}")
        launcher.trigger(hotkey_name)


def on_release(key):
    global ctrl_pressed

    if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        ctrl_pressed = False


def run_daemon():
    print("Desktop Hotkey Launcher running in background.")
    print("Press Ctrl+1..Ctrl+9, Ctrl+0, Ctrl+- or Ctrl+= to trigger actions.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    run_daemon()
