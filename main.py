import os
from sys import exit as sysexit
import tkinter as tk

from requests import get

from gui import Gui
from updater import Updater
from utils import PLAT_WIN, PLAT_NIX, PLAT_MAC

if not PLAT_WIN and not PLAT_NIX and not PLAT_MAC:
    print("OS is not supported!")
    sysexit(1)

print("Starting...")

if PLAT_WIN:
    ctypes = __import__('ctypes')
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

def ensure_needed_files():
    if not os.path.isfile("logo.png"):
        r = get("https://raw.githubusercontent.com/Tycho10101/LaunchiCube/refs/heads/main/logo.png", timeout=60)
        with open("logo.png", "wb") as f:
            f.write(r.content)

    def ensure_dir(name):
        if not os.path.isdir(name):
            os.mkdir(name)
            
    def ensure_file(name, contents=""):
        if not os.path.isfile(name):
            with open(name, "w") as f:
                f.write(contents)

    ensure_dir("clients")
    ensure_dir("instances")
    ensure_file("accounts.json", '{"accounts": [], "Selected Account": null}')
    ensure_file("instances/index.json", '[]')
    ensure_file("clients/index.json", '{"release_ver": "0.0", "dev_ver": 0}')

if __name__ == "__main__":
    ensure_needed_files()
    Updater.update_clients()

    root = tk.Tk()
    app = Gui(root)
    root.mainloop()
