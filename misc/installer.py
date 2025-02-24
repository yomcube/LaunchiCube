import os
import subprocess
from sys import exit as sysexit
import threading

from utils import get, save_link_as_file

HAS_TKINTER = False
while not HAS_TKINTER:
    try:
        import tkinter as tk
        from tkinter import ttk
        HAS_TKINTER = True
    except:
        print("It appears that I can't use tkinter.")
        print("To install this, use the respective command below:")
        print("""For Windows you need to reinstall python
For Linux use: sudo apt install python3-tk
For MacOS use: brew install python3-tk""")
        print("")
        HAS_TKINTER = False
    if not HAS_TKINTER:
        input("Press enter to try again.")

def test_libraries(libraries):
    missing_libraries = []
    for lib in libraries:
        try:
            exec(lib['import'])
        except:
            missing_libraries.append(lib)
            
    if not missing_libraries:
        missing_libraries.append(
            {"name": "None!", "description": "There is no missing libraries! You can now install!"}
        )
    return missing_libraries
        

class Installer:
    def __init__(self, root):
        self.root = root
        self.root.title("LaunchiCube Installer")
        self.root.geometry("420x420")
        self.root.configure(bg="#2C2F33")

        tk.Label(root, text="Missing Libraries:", bg="#2C2F33", fg="white").pack(pady=5, padx=5, anchor="nw")

        frame = tk.Frame(root, bg="#2C2F33")
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(frame, bg="#2C2F33", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2C2F33")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.required_libraries = [
            {
                "name": "Pillow",
                "description": """This is required to load and modify images.
To install this, use the respective command below:
For Windows use: pip install pillow
For Linux use: sudo apt install python3-pillow
For MacOS use: brew install python3-pillow""",
                "import": "from PIL import Image"
            },
            {
                "name": "Pillow-tk",
                "description": """This is required for pillow to talk to tkinter.
To install this, use the respective command below:
For Windows use: pip install pillow.imagetk
For Linux use: sudo apt install python3-pillow.imagetk
For MacOS use: brew install python3-pillow.imagetk""",
                "import": "from PIL import ImageTk"
            },
            {
                "name": "Requests",
                "description": """This is required for LaunchiCube to talk to the internet.
To install this, use the respective command below:
For Windows use: pip install requests
For Linux use: sudo apt install python3-requests
For MacOS use: brew install python3-requests""",
                "import": "import requests"
            },
        ]
        
        self.missing_libraries = test_libraries(self.required_libraries)

        self.library_entries = []

        self.populate_libraries()

        self.action_button = tk.Button(
            root, text="Install LaunchiCube", command=self.install_launchicube,
            bg="#7289DA", fg="white", font=("Arial", 12, "bold")
        )
        self.action_button.pack(pady=5)

        self.recheck_button = tk.Button(
            root, text="Recheck Libraries", command=self.recheck_libraries,
            bg="#FF5555", fg="white", font=("Arial", 12, "bold")
        )
        self.recheck_button.pack(pady=5)
        
        self.timer = None

    def populate_libraries(self):
        for lib in self.missing_libraries:
            entry_frame = tk.Frame(self.scrollable_frame, bg="#23272A", padx=10, pady=5)
            entry_frame.pack(fill="x", padx=5, pady=5)

            tk.Label(
                entry_frame, text=lib["name"], fg="white", bg="#23272A", font=("Arial", 12, "bold")
            ).pack(anchor="w")
            tk.Label(
                entry_frame, text=lib["description"], fg="white", bg="#23272A", justify="left", wraplength=950
            ).pack(anchor="w")

            self.library_entries.append(entry_frame)

    def clear_libraries(self):
        for entry in self.library_entries:
            entry.destroy()
        self.library_entries.clear()
        
    def recheck_libraries(self):
        self.missing_libraries = test_libraries(self.required_libraries)
        self.clear_libraries()
        self.library_entries = []
        self.populate_libraries()

    def install_launchicube(self):
        self.recheck_libraries()
        if self.missing_libraries == [
            {"name": "None!", "description": "There is no missing libraries! You can now install!"}
        ]:
            linkbase = "https://raw.githubusercontent.com/Tycho10101/LaunchiCube/refs/heads/main/"
            utils.save_link_as_file(f"{linkbase}misc/installer_backend.py", "installer_backend.py")
            installer_backend = __import__('installer_backend')
            installer_backend.install()
            os.remove("installer_backend.py")
            os.remove("installer.py")
            subprocess.Popen(["python", "main.py"])
            sysexit()
        else:
            def fix():
                self.action_button.config(text="Install LaunchiCube")
            self.action_button.config(text="There are still missing libraries!")
            try:
                self.timer.cancel()
            except:
                pass
            self.timer = threading.Timer(2, fix)
            self.timer.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = Installer(root)
    root.mainloop()
