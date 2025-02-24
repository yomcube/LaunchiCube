import os
import tkinter as tk

from gui import Gui
import updater
from utils import PLAT_WIN, PLAT_NIX, PLAT_MAC, get

if not PLAT_WIN and not PLAT_NIX and not PLAT_MAC:
    print("OS is not supported!")
    __import__('sys').exit()

print("Starting...")

if PLAT_WIN:
    ctypes = __import__('ctypes')
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

def ensure_needed_files():
    if not os.path.isfile("logo.png"):
        r = get("https://raw.githubusercontent.com/Tycho10101/LaunchiCube/refs/heads/main/logo.png")
        with open("logo.png", "wb") as f:
            f.write(r.content)

    def ensure_dir(name):
        if not os.path.isdir(name):
            os.mkdir(name)
            
    def ensure_file(name, contents=""):
        if not os.path.isfile(name):
            with open(name, "w", encoding="utf-8") as f:
                f.write(contents)

    ensure_dir("clients")
    ensure_dir("instances")
    ensure_file("accounts.json", '{"accounts": [], "Selected Account": null}')
    ensure_file("instances/index.json", '[]')
    ensure_file("clients/index.json", '{"release_ver": "0.0", "dev_ver": 0}')

if __name__ == "__main__":
    ensure_needed_files()
    updater.update_clients()

    root = tk.Tk()
    app = Gui(root)
    root.mainloop()
