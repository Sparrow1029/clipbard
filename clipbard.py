import os
import sys
import json
from json.decoder import JSONDecodeError

import PySimpleGUI as sg
import PySimpleGUIQt as sgQt
import pyperclip


# Check if we are a frozen pyinstaller bundle, or running as Python script
is_frozen = getattr(sys, "frozen", False)
frozen_temp_path = getattr(sys, "_MEIPASS", "")
if is_frozen:
    basedir = frozen_temp_path
else:
    basedir = os.path.dirname(os.path.abspath(__file__))


THEME = "Dark Blue 3"
# Uncomment to set color theme for windowed app
# sg.change_look_and_feel(THEME)
ICON_FP = os.path.join(basedir, "resources", "icon-filled.txt")
ICON = bytes(open(ICON_FP).read(), "utf-8")

HISTFILEPATH = os.path.expanduser("~/.cliphistory.json")
GREETING = """\
Well met, adventurer! I am a humble preview window.
Select an option from the menu to my left, and it will be copied \
to your system's clipboard... whatever that may be!

If you yet have no clipboard entries, copy some text and it will appear thence!"""


def get_data_from_file(file_obj=HISTFILEPATH):
    # Open and parse current history file
    if not os.path.exists(HISTFILEPATH):
        print("NO FILE")
        data = {"entries": []}
        with open(HISTFILEPATH, "w") as outfile:
            json.dump(data, outfile)

    try:
        with open(HISTFILEPATH, "r") as hf:
            data = json.load(hf)
    except JSONDecodeError as e:
        print(f"Error decoding json: {e}")
        data = {"entries": []}

    return data


def update_and_write(data, new_entry=None):
    global window

    if new_entry is not None:
        data["entries"].append(new_entry)
        with open(HISTFILEPATH, "w") as hf:
            json.dump(data, hf)
    window["-HIST-"].update(values=data["entries"])

    preview = new_entry or GREETING
    window["-PREV-"].update(value=preview)


def app(data, window, tray):

    selected = pyperclip.paste()
    window_hidden = False

    if not data["entries"]:
        update_and_write(data, new_entry=selected)

    while True:
        # System tray app
        menu_item = tray.read(timeout=50)
        if menu_item == "Exit":
            break
        elif menu_item == "Hide":
            if not window_hidden:
                window_hidden = True
                window.Hide()
        elif menu_item == "Show":
            if window_hidden:
                window_hidden = False
                window.UnHide()

        # Windowed app
        event, values = window.read(timeout=50)

        if event in (None, "Exit"):
            with open(HISTFILEPATH, "w") as hf:
                json.dump(data, hf)
            break

        if event == "Clear":
            data["entries"] = []
            update_and_write(data)
            continue

        if event == "Hide":
            window_hidden = True
            window.Hide()
            continue

        if pyperclip.paste() != selected:
            selected = pyperclip.paste()
            update_and_write(data, new_entry=selected)
            continue

        if not values["-HIST-"]:  # No options selected yet
            continue

        selected = values["-HIST-"][0]
        if selected == pyperclip.paste():
            continue
        update_and_write(data, new_entry=selected)
        pyperclip.copy(selected)

    window.close()
    tray.close()


if __name__ == "__main__":
    # set global data variables
    data = get_data_from_file()

    # Define layout for our windowed Application
    WINDOW_LAYOUT = [
        [sg.Text("Sing tales of the entries from clipboards past...")],
        [sg.Listbox(
            values=data["entries"],
            size=(30, 20),
            key="-HIST-",
            tooltip="Select an entry to copy to clipboard",
            enable_events=True),  # bind_return_key=True),
         sg.Multiline(
            size=(70, 21),
             key="-PREV-",
             default_text=GREETING,
            tooltip="Preview", disabled=True)],
        # [sg.Button("Update"), sg.Button("Clear"), sg.Button("Exit")]
        [sg.Button("Clear"),
         sg.Button("Hide", pad=((325, 0), (0, 0))),
         sg.Button("Exit")]
    ]

    SYS_MENU = ["TRAY", ["&Show", "&Hide", "---", "E&xit"]]

    # Initialize System Tray and Window
    tray = sgQt.SystemTray(menu=SYS_MENU, tooltip="Clipbard", data_base64=ICON)
    tray.ShowMessage("Clipbard", "Clipbard is running!", time=3000)
    window = sg.Window(
        "Clipbard",
        icon=ICON,
        return_keyboard_events=True,
        disable_close=True).Layout(WINDOW_LAYOUT)
    window.Finalize()

    app(data, window, tray)
