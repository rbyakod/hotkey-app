#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
LABEL="com.ravibyakod.hotkey-app"
PLIST_PATH="$HOME/Library/LaunchAgents/${LABEL}.plist"
LOG_DIR="$REPO_ROOT/logs"
PYTHON_BIN="${REPO_ROOT}/.venv/bin/python"

if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="$(python3 -c 'import sys; print(sys.executable)')"
fi

mkdir -p "$HOME/Library/LaunchAgents" "$LOG_DIR"

cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${LABEL}</string>

  <key>ProgramArguments</key>
  <array>
    <string>${PYTHON_BIN}</string>
    <string>${REPO_ROOT}/hotkey_daemon.py</string>
  </array>

  <key>WorkingDirectory</key>
  <string>${REPO_ROOT}</string>

  <key>RunAtLoad</key>
  <true/>

  <key>KeepAlive</key>
  <true/>

  <key>ProcessType</key>
  <string>Interactive</string>

  <key>LimitLoadToSessionType</key>
  <array>
    <string>Aqua</string>
  </array>

  <key>StandardOutPath</key>
  <string>${LOG_DIR}/hotkey-daemon.log</string>

  <key>StandardErrorPath</key>
  <string>${LOG_DIR}/hotkey-daemon.error.log</string>
</dict>
</plist>
EOF

launchctl bootout "gui/$(id -u)" "$PLIST_PATH" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$PLIST_PATH"
launchctl enable "gui/$(id -u)/${LABEL}"
launchctl kickstart -k "gui/$(id -u)/${LABEL}"

cat <<EOF
Installed LaunchAgent: ${LABEL}
Plist: ${PLIST_PATH}
Python: ${PYTHON_BIN}

The daemon will now start at login.
If macOS blocks key monitoring, grant Accessibility permissions to your terminal app and the selected Python binary.
Logs:
  ${LOG_DIR}/hotkey-daemon.log
  ${LOG_DIR}/hotkey-daemon.error.log
EOF
