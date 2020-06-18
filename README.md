# Clipbard
### A clipboard history desktop app

- Built using PySimpleGUI / PySimpleGUIQt / pyperclip
- Can be compiled into binary/executable using pyinstaller to be cross-platform, standalone desktop application

## Usage
1. create a virtual environment using Python 3.6+
2. `(venv)$ pip install -r requirements.txt`
3. `(venv)$ python clipboard.py`

The app runs with a window and system tray icon.

## To build desktop app (so far, only tested on Lubuntu 18.04LTS)
1. `(venv)$ pip install pyinstaller` inside your virtual environment
2. `(venv)$ pyinstaller --add-data "resources/*:resources" --onefile clipbard.py`
  - Optionally, for Windows/MacOS you can convert one of the .png files in the `resources` directory into a `.ico` or `.icns`
  - Then you can pass the argument `-i resources/<icon file>.icns (or .ico for Windows)` to give the resulting app bundle an icon
3. The `--onefile` argument makes a `dist/` directory containing a single, executable binary `clipbard`


### TODO:
- [ ] Incorporate a RDBMS system like SQLite3 (instead of simple JSON file) to add dates, hashing, etc to history data
- [ ] Test functionality with Windows / MacOS
- [ ] Once RDBM is used, make clipboard history searchable (fuzzy/elasticsearch?)
- [ ] Allow users to add manual entries to clipboard
- [ ] Edit (and re-order?) entries
