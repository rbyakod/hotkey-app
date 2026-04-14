#!/usr/bin/env bash
set -euo pipefail

LABEL="com.ravibyakod.hotkey-app"
PLIST_PATH="$HOME/Library/LaunchAgents/${LABEL}.plist"
SERVICE="gui/$(id -u)/${LABEL}"

if [[ ! -f "$PLIST_PATH" ]]; then
  echo "LaunchAgent is not installed."
  echo "Run ./install_launch_agent.sh first."
  exit 1
fi

launchctl bootstrap "gui/$(id -u)" "$PLIST_PATH" >/dev/null 2>&1 || true
launchctl enable "$SERVICE"
launchctl kickstart -k "$SERVICE"

echo "Started daemon: ${LABEL}"
