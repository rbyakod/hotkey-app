# Hotkey App

This app has two parts:

- `hotkey_web_config.py`: local Flask UI to configure hotkey mappings
- `hotkey_daemon.py`: background listener that reacts to the configured hotkeys

## Setup

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask pynput
chmod +x install_launch_agent.sh uninstall_launch_agent.sh status_launch_agent.sh start_config_gui.sh start_daemon.sh stop_daemon.sh
```

## Run The Config GUI

Start the local Flask UI:

```bash
./start_config_gui.sh
```

Then open:

```text
http://127.0.0.1:5050
```

Use this page to add, change, or clear hotkey mappings.
Changes take effect immediately in the running daemon. You do not need to restart it after updating a mapping.

## Run The Daemon Manually

Start the background hotkey listener in a terminal:

```bash
source .venv/bin/activate
python3 hotkey_daemon.py
```

This listens for:

- `Ctrl+1` through `Ctrl+9`
- `Ctrl+0`
- `Ctrl+-`
- `Ctrl+=`

## Install To Run At Login

On macOS, use a `LaunchAgent`, not a `LaunchDaemon`. The hotkey listener needs your logged-in GUI session.

Install and start the background process:

```bash
./install_launch_agent.sh
```

This registers:

```text
~/Library/LaunchAgents/com.ravibyakod.hotkey-app.plist
```

The installer also starts the daemon immediately and configures it to launch automatically on login.

## Start The Background Daemon

Start or restart the installed LaunchAgent with:

```bash
./start_daemon.sh
```

## Stop The Background Daemon

Stop the installed LaunchAgent with:

```bash
./stop_daemon.sh
```

## Uninstall The Background Process

Remove the login agent with:

```bash
./uninstall_launch_agent.sh
```

## Check Status

Check whether the background agent is loaded and whether `hotkey_daemon.py` is running:

```bash
./status_launch_agent.sh
```

## Logs

The background agent writes logs to:

- `logs/hotkey-daemon.log`
- `logs/hotkey-daemon.error.log`

## macOS Permissions

For `pynput` to capture global shortcuts, macOS may require Accessibility permission for:

- your terminal app while testing manually
- the Python interpreter used by the LaunchAgent

The installer resolves `.venv/bin/python` to the real Python executable before writing the LaunchAgent plist. This matters because macOS privacy permissions can treat symlinks and the real executable as different apps.

If you see this error in the log:

```text
This process is not trusted! Input event monitoring will not be possible until it is added to accessibility clients.
```

macOS has not approved the Python binary running the daemon. Approve the exact interpreter path printed by `./install_launch_agent.sh`, for example:

```text
/Users/your-user-name/.pyenv/versions/3.12.0/bin/python3.12
```

Check both panes:

- System Settings > Privacy & Security > Accessibility
- System Settings > Privacy & Security > Input Monitoring

If the file picker shows `python` or `python3` grayed out, choose the real versioned binary, such as `python3.12`.

If the daemon appears to be running but shortcuts do nothing, also check:

- System Settings > Privacy & Security > Accessibility
- System Settings > Privacy & Security > Input Monitoring
- `logs/hotkey-daemon.error.log`

## Finder Window Fix

Finder is special-cased in `hotkey_launcher.py`.

The old behavior always created a new Finder window. The first fix changed Finder to reuse an existing window, but that exposed another macOS detail: Finder can have an existing window that is minimized. In that case the menu bar changes to Finder, but no visible window appears.

Current behavior:

- If Finder has no windows, create a new Home window.
- If Finder has an existing window, unminimize it and bring it to the front.
- Pressing the Finder hotkey repeatedly should not create duplicate windows.

## How To Install This On A Different Or New Computer

Use these steps on the new Mac.

1. Clone or copy this repo:

```bash
git clone <repo-url> hotkey-app
cd hotkey-app
```

2. Create the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask pynput
```

3. Make scripts executable:

```bash
chmod +x install_launch_agent.sh uninstall_launch_agent.sh status_launch_agent.sh start_config_gui.sh start_daemon.sh stop_daemon.sh
```

4. Start the config GUI:

```bash
./start_config_gui.sh
```

5. Open the local config page:

```text
http://127.0.0.1:5050
```

6. Configure hotkeys, for example:

```text
Ctrl+1 -> finder
Ctrl+2 -> TextEdit
Ctrl+3 -> YouTube
Ctrl+4 -> calculator
```

7. Install the LaunchAgent:

```bash
./install_launch_agent.sh
```

8. Copy the exact Python path printed by the installer. It will look like one of these:

```text
/Users/your-user-name/.pyenv/versions/3.12.0/bin/python3.12
/Users/your-user-name/WORK/hotkey-app/.venv/bin/python3.12
```

9. Approve that Python binary in Accessibility:

- Open System Settings.
- Go to Privacy & Security.
- Open Accessibility.
- Click `+`.
- Press `Cmd+Shift+G` in the file picker.
- Paste the folder path that contains the printed Python binary.
- Select the real versioned Python file, such as `python3.12`.
- Click Open.
- Turn the toggle on.

10. Approve the same Python binary in Input Monitoring:

- Go back to Privacy & Security.
- Open Input Monitoring.
- Click `+`.
- Press `Cmd+Shift+G`.
- Paste the same folder path.
- Select the same Python file.
- Click Open.
- Turn the toggle on.

11. Restart the daemon:

```bash
./start_daemon.sh
```

12. Check status and logs:

```bash
./status_launch_agent.sh
tail -80 logs/hotkey-daemon.error.log
tail -80 logs/hotkey-daemon.log
```

13. Test the configured hotkeys:

- Press `Ctrl+1` for Finder.
- Press the other configured shortcuts.
- If Finder focuses but no window appears, restart the daemon and test again:

```bash
./start_daemon.sh
```
