# Hotkey App

This app has two parts:

- `hotkey_web_config.py`: local Flask UI to configure hotkey mappings
- `hotkey_daemon.py`: background listener that reacts to the configured hotkeys

## Run Manually

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask pynput
python3 hotkey_web_config.py
```

Open `http://127.0.0.1:5000` and add your mappings.

In another terminal:

```bash
source .venv/bin/activate
python3 hotkey_daemon.py
```

## Run At Login On macOS

Use a `LaunchAgent`, not a `LaunchDaemon`. The hotkey listener needs your logged-in GUI session.

1. Create the virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask pynput
```

2. Install the login agent:

```bash
chmod +x install_launch_agent.sh uninstall_launch_agent.sh
./install_launch_agent.sh
```

3. Configure mappings with:

```bash
source .venv/bin/activate
python3 hotkey_web_config.py
```

The installer registers `~/Library/LaunchAgents/com.ravibyakod.hotkey-app.plist` and starts the daemon immediately.

## Logs

The login agent writes logs to:

- `logs/hotkey-daemon.log`
- `logs/hotkey-daemon.error.log`

## Remove The Login Agent

```bash
./uninstall_launch_agent.sh
```

## macOS Permissions

For `pynput` to capture global shortcuts, macOS may require Accessibility permission for:

- your terminal app while testing manually
- the Python interpreter used by the LaunchAgent

If the daemon appears to be running but shortcuts do nothing, check:

- System Settings > Privacy & Security > Accessibility
- `logs/hotkey-daemon.error.log`
