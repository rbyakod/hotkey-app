#!/usr/bin/env bash
set -euo pipefail

LABEL="com.ravibyakod.hotkey-app"
SERVICE="gui/$(id -u)/${LABEL}"

echo "LaunchAgent status for ${LABEL}"
echo

if launchctl print "$SERVICE" >/tmp/hotkey-app-launchctl-status.txt 2>/dev/null; then
  grep -E "^\s*state = " /tmp/hotkey-app-launchctl-status.txt || true
  echo
  echo "Service is loaded in launchd."
else
  echo "Service is not loaded in launchd."
fi

echo
echo "Matching processes:"
if ps -ax | grep -F "hotkey_daemon.py" | grep -v grep; then
  :
else
  echo "No running hotkey_daemon.py process found."
fi
