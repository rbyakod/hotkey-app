#!/usr/bin/env bash
set -euo pipefail

LABEL="com.ravibyakod.hotkey-app"
PLIST_PATH="$HOME/Library/LaunchAgents/${LABEL}.plist"

if [[ ! -f "$PLIST_PATH" ]]; then
  echo "LaunchAgent is not installed."
  exit 1
fi

launchctl bootout "gui/$(id -u)" "$PLIST_PATH" >/dev/null 2>&1 || true

echo "Stopped daemon: ${LABEL}"
