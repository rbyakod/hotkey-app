# hotkey_daemon.py
import platform
import subprocess
import sys
import time
from ctypes import CDLL, c_bool
from ctypes.util import find_library

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


def is_accessibility_trusted() -> bool:
    if platform.system() != "Darwin":
        return True

    app_services = CDLL(find_library("ApplicationServices"))
    app_services.AXIsProcessTrusted.restype = c_bool
    return bool(app_services.AXIsProcessTrusted())


def open_privacy_settings():
    if platform.system() != "Darwin":
        return

    panes = [
        "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility",
        "x-apple.systempreferences:com.apple.preference.security?Privacy_ListenEvent",
    ]
    for pane in panes:
        try:
            subprocess.Popen(["open", pane])
        except OSError:
            pass


def wait_for_macos_permissions() -> bool:
    if is_accessibility_trusted():
        return True

    print("Hotkey daemon cannot start because macOS has not trusted this process yet.", file=sys.stderr)
    print(f"Grant access to this Python binary: {sys.executable}", file=sys.stderr)
    print(
        "Open System Settings > Privacy & Security and enable this binary under Accessibility "
        "and Input Monitoring if macOS lists it there.",
        file=sys.stderr,
    )
    open_privacy_settings()
    print("Waiting for permission approval in System Settings...", file=sys.stderr)

    while not is_accessibility_trusted():
        time.sleep(5)

    print("macOS permissions granted. Starting hotkey listener.", file=sys.stderr)
    return True


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
    if not wait_for_macos_permissions():
        return

    print("Desktop Hotkey Launcher running in background.")
    print("Press Ctrl+1..Ctrl+9, Ctrl+0, Ctrl+- or Ctrl+= to trigger actions.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    run_daemon()
