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

If you see this error in the log:

```text
This process is not trusted! Input event monitoring will not be possible until it is added to accessibility clients.
```

macOS has not approved the Python binary running the daemon. Approve the exact interpreter path used by the LaunchAgent, typically:

```text
/Users/your-user-name/WORK/hotkey-app/.venv/bin/python
```

Check both panes:

- System Settings > Privacy & Security > Accessibility
- System Settings > Privacy & Security > Input Monitoring

If the daemon appears to be running but shortcuts do nothing, also check:

- System Settings > Privacy & Security > Accessibility
- `logs/hotkey-daemon.error.log`
