# hotkey_launcher.py
import json
import os
import platform
import subprocess
import tempfile
import webbrowser
from typing import Dict

CONFIG_PATH = os.path.expanduser("~/.desktophotkeys.json")
AVAILABLE_HOTKEYS = [
    "ctrl+1",
    "ctrl+2",
    "ctrl+3",
    "ctrl+4",
    "ctrl+5",
    "ctrl+6",
    "ctrl+7",
    "ctrl+8",
    "ctrl+9",
    "ctrl+0",
    "ctrl+-",
    "ctrl+=",
]
LEGACY_HOTKEY_MAP = {
    "fn+1": "ctrl+1",
    "fn+2": "ctrl+2",
    "fn+3": "ctrl+3",
    "fn+4": "ctrl+4",
    "fn+5": "ctrl+5",
    "fn+6": "ctrl+6",
    "fn+7": "ctrl+7",
    "fn+8": "ctrl+8",
    "fn+9": "ctrl+9",
    "fn+10": "ctrl+0",
    "fn+11": "ctrl+-",
    "fn+12": "ctrl+=",
}


class HotkeyLauncher:
    def __init__(self):
        self.app_mappings = self._init_app_mappings()
        self.hotkey_mappings = {}
        self._config_version = None
        self._load_config(force=True)

    def _init_app_mappings(self) -> Dict[str, str]:
        # reuse / copy from voice_app_launcher.py
        return {
            "youtube": "https://www.youtube.com",
            "gmail": "https://mail.google.com",
            "google": "https://www.google.com",
            "github": "https://github.com",
            "calculator": "Calculator",
            "notes": "Notes",
            "terminal": "Terminal",
            "finder": "Finder",
            # add more as needed
        }

    def _get_config_version(self):
        if not os.path.exists(CONFIG_PATH):
            return None
        return os.stat(CONFIG_PATH).st_mtime_ns

    def _load_config(self, force: bool = False) -> Dict[str, str]:
        config_version = self._get_config_version()
        if not force and config_version == self._config_version:
            return dict(self.hotkey_mappings)

        if config_version is None:
            self.hotkey_mappings = {}
            self._config_version = None
            return {}

        with open(CONFIG_PATH, "r") as f:
            hotkey_mappings = json.load(f)

        migrated_mappings = {}
        changed = False
        for hotkey, target in hotkey_mappings.items():
            migrated_hotkey = LEGACY_HOTKEY_MAP.get(hotkey, hotkey)
            if migrated_hotkey != hotkey:
                changed = True
            migrated_mappings[migrated_hotkey] = target

        self.hotkey_mappings = migrated_mappings
        self._config_version = config_version

        if changed:
            self._save_config()

        return dict(self.hotkey_mappings)

    def _save_config(self):
        config_dir = os.path.dirname(CONFIG_PATH) or "."
        os.makedirs(config_dir, exist_ok=True)

        fd, temp_path = tempfile.mkstemp(prefix=".desktophotkeys.", suffix=".json", dir=config_dir)
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(self.hotkey_mappings, f, indent=2)
            os.replace(temp_path, CONFIG_PATH)
        except Exception:
            try:
                os.unlink(temp_path)
            except FileNotFoundError:
                pass
            raise

        self._config_version = self._get_config_version()

    def _open_finder_home(self):
        subprocess.Popen([
            "osascript",
            "-e",
            'tell application "Finder"',
            "-e",
            "activate",
            "-e",
            "set finder_window to make new Finder window",
            "-e",
            "set target of finder_window to home",
            "-e",
            "end tell",
        ])

    def set_hotkey(self, hotkey: str, target_key: str):
        # hotkey like "ctrl+1", target_key like "youtube" or "calculator"
        self._load_config()
        self.hotkey_mappings[hotkey] = target_key
        self._save_config()

    def remove_hotkey(self, hotkey: str):
        self._load_config()
        if hotkey in self.hotkey_mappings:
            del self.hotkey_mappings[hotkey]
            self._save_config()

    def list_hotkeys(self):
        self._load_config()
        return dict(self.hotkey_mappings)

    def trigger(self, hotkey: str):
        """Called when a hotkey is pressed."""
        self._load_config()
        target_key = self.hotkey_mappings.get(hotkey)
        if not target_key:
            return
        self._open_target(target_key)

    def _open_target(self, target: str):
        key = target.lower()
        if key in self.app_mappings:
            value = self.app_mappings[key]
            if value.startswith("http"):
                webbrowser.open(value)
            else:
                if platform.system() == "Darwin":
                    if value == "Finder":
                        self._open_finder_home()
                    else:
                        subprocess.Popen(["open", "-a", value])
                else:
                    # only macOS for now
                    pass
        else:
            # if value is a raw URL or app
            if target.startswith("http"):
                webbrowser.open(target)
            else:
                if platform.system() == "Darwin":
                    if key == "finder":
                        self._open_finder_home()
                    else:
                        subprocess.Popen(["open", "-a", target])
