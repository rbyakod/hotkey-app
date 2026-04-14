# hotkey_web_config.py
from flask import Flask, render_template_string, request, redirect, url_for, flash
from hotkey_launcher import AVAILABLE_HOTKEYS, HotkeyLauncher

HOST = "127.0.0.1"
PORT = 5050

app = Flask(__name__)
app.secret_key = "change-me-dev-only"

launcher = HotkeyLauncher()

TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Desktop Hotkeys</title>
  <style>
    body { font-family: sans-serif; max-width: 640px; margin: 20px auto; }
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th, td { border: 1px solid #ccc; padding: 6px 8px; }
    th { background: #f2f2f2; }
    .flash { padding: 8px; margin: 8px 0; border-radius: 4px; }
    .flash-error { background: #ffe5e5; border: 1px solid #ff9999; }
    .flash-success { background: #e5ffe5; border: 1px solid #99ff99; }
  </style>
</head>
<body>
  <h1>Desktop Hotkey Config</h1>

  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      {% for category, msg in messages %}
        <div class="flash flash-{{category}}">{{ msg }}</div>
      {% endfor %}
    {% endif %}
  {% endwith %}

  <h2>Current mappings</h2>
  <table>
    <tr>
      <th>Hotkey</th>
      <th>Target</th>
      <th>Action</th>
    </tr>
    {% for hk in available_hotkeys %}
      <tr>
        <td>{{ hk }}</td>
        <td>{{ mappings.get(hk, '-') }}</td>
        <td>
          {% if mappings.get(hk) %}
            <form method="post" action="{{ url_for('delete_mapping') }}" style="display:inline;">
              <input type="hidden" name="hotkey" value="{{ hk }}">
              <button type="submit">Clear</button>
            </form>
          {% else %}
            -
          {% endif %}
        </td>
      </tr>
    {% endfor %}
  </table>

  <h2>Assign / change hotkey</h2>
  <form method="post" action="{{ url_for('set_mapping') }}">
    <label>Hotkey:
      <select name="hotkey">
        {% for hk in available_hotkeys %}
        <option value="{{ hk }}">{{ hk }}</option>
        {% endfor %}
      </select>
    </label>
    <br><br>
    <label>Target key (from app_mappings or URL/app name):<br>
      <input type="text" name="target" size="40" required>
    </label>
    <br><br>
    <button type="submit">Save mapping</button>
  </form>

  <p>Shortcuts use Ctrl with 1-9, 0, -, and =. Examples: "youtube", "gmail", "calculator", "https://example.com", "Safari".</p>
</body>
</html>
"""

@app.route("/")
def index():
    mappings = launcher.list_hotkeys()
    return render_template_string(
        TEMPLATE,
        mappings=mappings,
        available_hotkeys=AVAILABLE_HOTKEYS
    )

@app.route("/set", methods=["POST"])
def set_mapping():
    hotkey = request.form.get("hotkey")
    target = request.form.get("target", "").strip()

    if not hotkey or not target:
        flash(("error", "Hotkey and target are required."))
        return redirect(url_for("index"))

    # check duplicate target assignment if you want to avoid one target with many keys
    # here we just ensure that a hotkey exists at most once (already guaranteed by dict)
    # but we also check if same target is already mapped to some other key (optional)
    existing = launcher.list_hotkeys()
    for hk, tg in existing.items():
        if hk != hotkey and tg == target:
            flash(("error", f"Target '{target}' is already assigned to {hk}."))
            return redirect(url_for("index"))

    launcher.set_hotkey(hotkey, target)
    flash(("success", f"Assigned {hotkey} → {target}."))
    return redirect(url_for("index"))

@app.route("/delete", methods=["POST"])
def delete_mapping():
    hotkey = request.form.get("hotkey")
    if hotkey:
        launcher.remove_hotkey(hotkey)
        flash(("success", f"Cleared mapping for {hotkey}."))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(HOST, PORT, debug=True)
