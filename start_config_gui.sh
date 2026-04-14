#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
PYTHON_BIN="${REPO_ROOT}/.venv/bin/python"

if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="$(python3 -c 'import sys; print(sys.executable)')"
fi

exec "$PYTHON_BIN" "${REPO_ROOT}/hotkey_web_config.py"
