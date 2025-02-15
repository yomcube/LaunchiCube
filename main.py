from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import os
import json
import re
from zipfile import ZipFile
from tarfile import TarFile
import io
import requests
import math
import subprocess
import sys
import ctypes
import base64

try:
    import ctypes.wintypes
    crypt32 = ctypes.windll.crypt32

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_ubyte))]

    def encrypt_data(data: bytes) -> bytes:
        blob_in = DATA_BLOB(len(data), ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_ubyte)))
        blob_out = DATA_BLOB()
        
        if crypt32.CryptProtectData(
            ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)
        ):
            encrypted_bytes = ctypes.string_at(blob_out.pbData, blob_out.cbData)
            ctypes.windll.kernel32.LocalFree(blob_out.pbData)
            return base64.b64encode(encrypted_bytes).decode("utf-8")
        else:
            raise RuntimeError(f"Encryption failed. Error Code: {ctypes.windll.kernel32.GetLastError()}")
finally:
    pass

print("Starting...")

LOGO_SIZE = (150, 150)
MAX_TEXT_WIDTH = 140

last_instances_columns = 1

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
finally:
    pass

def ensure_needed_files():
    if not os.path.isfile("logo.png"):
        r = requests.get("https://raw.githubusercontent.com/Tycho10101/LaunchiCube/refs/heads/main/logo.png")
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
            
class updater:
    def update_clients():
        r = requests.get("https://cdn.classicube.net/client/builds.json")
        f = json.loads(load_file("clients/index.json"))
        
        if not json.loads(r.text)["release_version"] == f["release_ver"]:
            print("Downloading Latest Release Version")
            f["release_ver"] = json.loads(r.text)["release_version"]
            save_file("clients/index.json", json.dumps(f))
            updater.download_release()
        
        if not json.loads(r.text)["latest_ts"] == f["dev_ver"]:
            print("Downloading Latest Dev Version")
            f["dev_ver"] = json.loads(r.text)["latest_ts"]
            save_file("clients/index.json", json.dumps(f))
            updater.download_dev()
             
    def download_release():
        is_64bit = sys.maxsize > 2**32
        
        if sys.platform == "win32" or sys.platform == "cygwin":
            if is_64bit:
                r = requests.get("https://cdn.classicube.net/client/release/win64/ClassiCube.zip")
            else:
                r = requests.get("https://cdn.classicube.net/client/release/win32/ClassiCube.zip")
            
            z = ZipFile(io.BytesIO(r.content))
            z.extract("ClassiCube/ClassiCube.exe", path="clients/temp/")
            if os.path.isfile("clients/Latest Stable Version.exe"):
                os.remove("clients/Latest Stable Version.exe")
            os.rename("clients/temp/ClassiCube/ClassiCube.exe", "clients/Latest Stable Version.exe")
            z.close()
            os.rmdir("clients/temp/ClassiCube")
            os.rmdir("clients/temp/")
        
        elif sys.platform == "darwin":
            if is_64bit:
                r = requests.get("https://cdn.classicube.net/client/release/osx64/ClassiCube.tar.gz")
            else:
                r = requests.get("https://cdn.classicube.net/client/release/osx32/ClassiCube.tar.gz")
                
            t = TarFile(io.BytesIO(r.content))
            t.extract("ClassiCube/ClassiCube", path="clients/temp/")
            if os.path.isfile("clients/Latest Stable Version"):
                os.remove("clients/Latest Stable Version")
            os.rename("clients/temp/ClassiCube/ClassiCube", "clients/Latest Stable Version")
            t.close()
            os.rmdir("clients/temp/ClassiCube")
            os.rmdir("clients/temp/")
            
        elif sys.platform == "linux":
            if is_64bit:
                r = requests.get("https://cdn.classicube.net/client/release/nix64/ClassiCube.tar.gz")
            else:
                r = requests.get("https://cdn.classicube.net/client/release/nix32/ClassiCube.tar.gz")
                
            t = TarFile(io.BytesIO(r.content))
            t.extract("ClassiCube/ClassiCube", path="clients/temp/")
            if os.path.isfile("clients/Latest Stable Version"):
                os.remove("clients/Latest Stable Version")
            os.rename("clients/temp/ClassiCube/ClassiCube", "clients/Latest Stable Version")
            t.close()
            os.rmdir("clients/temp/ClassiCube")
            os.rmdir("clients/temp/")
                
    def download_dev():
        r = requests.get("https://nightly.link/ClassiCube/ClassiCube/workflows/build_windows/master/ClassiCube-Win64-Direct3D9.exe.zip")
        z = ZipFile(io.BytesIO(r.content))
        z.extractall(path="clients/temp/")
        if os.path.isfile("clients/Latest Dev Version.exe"):
            os.remove("clients/Latest Dev Version.exe")
        os.rename("clients/temp/cc-w64-d3d9.exe", "clients/Latest Dev Version.exe")
        z.close()
        os.rmdir("clients/temp/")

def load_file(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    return ""

def save_file(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)

def get_safe_unique_filename(directory, filename):
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename).strip().replace(" ", "_")
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1

    return new_filename

def getVersions(version_type):
    return ["Latest Stable Version"] if version_type == "stable" else ["Latest Dev Version"]

def instanceNameExists(name):
    return any(i["name"] == name for i in json.loads(load_file("instances/index.json")))

def username_exists(name):
    return any(i["name"] == name for i in json.loads(load_file("accounts.json"))["accounts"])

def makeInstance(name, version):
    safe_unique_filename = get_safe_unique_filename("instances/", name)
    instances_json = json.loads(load_file("instances/index.json"))
    instances_json.append({"name": name, "ver": version, "dir": safe_unique_filename})
    save_file("instances/index.json", json.dumps(instances_json))
    os.mkdir(f"instances/{safe_unique_filename}")
    
def save_account(username, password):
    accounts_json = json.loads(load_file("accounts.json"))
    accounts_json["accounts"].append({"name": username, "password": encrypt_data(password.encode("utf-8"))})
    save_file("accounts.json", json.dumps(accounts_json))

def login_to_cc(username, password):
    session = requests.Session()
    r = session.get("https://www.classicube.net/api/login/")
    myobj = {"username": username, "password": password, "token": r.json()["token"]}
    x = session.post("https://www.classicube.net/api/login/", data=myobj)
    return [x.json()["authenticated"],x.json()["username"]]
    
def change_option(instance, option, value):
    f = load_file(f"instances/{instance}/options.txt")
    f = f.split("\n")
    where = None
    for i in range(len(f)):
        if f[i].startswith(f"{option}="):
            where = i
    
    if where == None:
        f.append(f"{option}={value}")
    else:
        f[where] = f"{option}={value}"
    save_file(f"instances/{instance}/options.txt", "\n".join(f))
    
def delete_option(instance, option):
    f = load_file(f"instances/{instance}/options.txt")
    f = f.split("\n")
    where = None
    for i in range(len(f)):
        if f[i].startswith(f"{option}="):
            where = i
    
    if not where == None:
        del f[where]
    
    save_file(f"instances/{instance}/options.txt", "\n".join(f))

ensure_needed_files()
updater.update_clients()
class LaunchiCubeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LaunchiCube")
        self.root.geometry("1200x750")
        self.root.configure(bg="#2C2F33")

        self.load_accounts()

        try:
            self.launcher_icon = ImageTk.PhotoImage(Image.open("logo.png").resize(LOGO_SIZE, Image.Resampling.LANCZOS))
            self.root.iconphoto(True, self.launcher_icon)
        except:
            print("logo.png not found!")
            self.launcher_icon = None

        self.top_frame = tk.Frame(root, bg="#3C3F41", height=50)
        self.top_frame.pack(fill="x")

        tk.Button(self.top_frame, text="Add Instance", command=self.open_add_instance,
                  bg="#7289DA", fg="white", font=("Arial", 12, "bold")).pack(pady=10, padx=10, side="left")

        self.right_frame = tk.Frame(root, bg="#3C3F41", width=250)
        self.right_frame.pack_propagate(False)
        self.right_frame.pack(fill="y", side="right")

        self.right_logo_label = tk.Label(self.right_frame, bg="#3C3F41")
        self.right_name_label = tk.Label(self.right_frame, bg="#3C3F41", fg="white", font=("Arial", 14, "bold"))
        self.play_button = tk.Button(self.right_frame, text="Play", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                                     command=lambda: self.start_game(self.selected_instance), state="disabled")

        self.main_frame = tk.Frame(root, bg="#23272A")
        self.main_frame.pack(expand=True, fill="both")
        self.main_frame.bind("<Configure>", self.on_resize)

        self.selected_instance = None
        self.load_instances()

        self.acc_switch_button = tk.Button(self.top_frame, text="Select an Option", command=self.show_menu, bg="#7289DA", fg="white", font=("Arial", 12, "bold"))
        self.acc_switch_button.pack(pady=10, padx=10, side="right")
        
        self.dropdown_window = None
        
        accounts_json = json.loads(load_file("accounts.json"))
        if not accounts_json["Selected Account"] == None:
            self.select_option(accounts_json["Selected Account"])

    def truncate_text(self, text, font, max_width):
        temp_text = text
        test_label = tk.Label(self.root, text=temp_text, font=font)
        test_label.update_idletasks()
        
        while test_label.winfo_reqwidth() > max_width and len(temp_text) > 1:
            temp_text = temp_text[:-1]
            test_label.config(text=temp_text + "...")
            test_label.update_idletasks()

        return temp_text + "..." if temp_text != text else text

    def on_resize(self, event=None):
        global last_instances_columns
        instances_columns = math.floor(self.main_frame.winfo_width()/195)
        if not instances_columns == last_instances_columns:
            if hasattr(self, "resize_after_id"):
                self.root.after_cancel(self.resize_after_id)
            self.resize_after_id = self.root.after(10, self.load_instances)
        last_instances_columns = instances_columns

    def select_instance(self, instance):
        logo_path = f"instances/{instance['dir']}/logo.png"

        if os.path.exists(logo_path):
            instance_icon = ImageTk.PhotoImage(Image.open(logo_path).resize(LOGO_SIZE, Image.Resampling.LANCZOS))
        else:
            instance_icon = self.launcher_icon

        self.instance_logo_label.config(image=instance_icon)
        self.instance_logo_label.image = instance_icon

        self.instance_name_label.config(text=instance["name"])

        self.play_button["state"] = "normal"
        self.play_button.config(command=lambda: self.start_game(instance))

    def start_game(self, instance):
        if instance:
            print(f"Starting game for: {instance['name']}")
            accounts_json = json.loads(load_file("accounts.json"))
            if not accounts_json["Selected Account"] == None:
                selected_account_pass = None
                for acc in accounts_json["accounts"]:
                    if acc["name"] == accounts_json["Selected Account"]:
                        selected_account_pass = acc["password"]
                        
                change_option(instance['dir'], "launcher-cc-username", accounts_json["Selected Account"])
                change_option(instance['dir'], "launcher-dc-username", accounts_json["Selected Account"])
                change_option(instance['dir'], "launcher-cc-password", selected_account_pass)
                delete_option(instance['dir'], "launcher-session")
                delete_option(instance['dir'], "launcher-server")
                delete_option(instance['dir'], "launcher-ip")
                delete_option(instance['dir'], "launcher-port")
                delete_option(instance['dir'], "launcher-mppass")
                delete_option(instance['dir'], "launcher-dc-mppass")
                
            if sys.platform == "darwin" or sys.platform == "linux":
                subprocess.run([f"clients/{instance['ver']}"], cwd=f'instances/{instance['dir']}/')
            else:
                subprocess.run([f"clients/{instance['ver']}.exe"], cwd=f'instances/{instance['dir']}/')

    def update_right_bar(self, instance):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        if not instance:
            return

        instance_dir = f"instances/{instance['dir']}"
        logo_path = f"{instance_dir}/logo.png"
        if os.path.exists(logo_path):
            instance_logo = ImageTk.PhotoImage(Image.open(logo_path).resize(LOGO_SIZE, Image.Resampling.LANCZOS))
        else:
            instance_logo = self.launcher_icon

        self.right_logo_label = tk.Label(self.right_frame, image=instance_logo, bg="#3C3F41")
        self.right_logo_label.image = instance_logo
        self.right_logo_label.pack(pady=20)

        self.right_name_label = tk.Label(self.right_frame, text=instance["name"], bg="#3C3F41",
                                         fg="white", font=("Arial", 14, "bold"))
        self.right_name_label.pack(pady=10)

        self.play_button = tk.Button(self.right_frame, text="Play", bg="#4CAF50", fg="white",
                                     font=("Arial", 12, "bold"), command=lambda: self.start_game(instance))
        self.play_button.pack(pady=10)

    def load_instances(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        instances = json.loads(load_file("instances/index.json"))

        num_columns = max(1, math.floor(self.main_frame.winfo_width() / 195))
        row, col = 0, 0

        for instance in instances:
            instance_dir = f"instances/{instance['dir']}"
            logo_path = f"{instance_dir}/logo.png"

            if os.path.exists(logo_path):
                instance_icon = ImageTk.PhotoImage(Image.open(logo_path).resize(LOGO_SIZE, Image.Resampling.LANCZOS))
            else:
                instance_icon = self.launcher_icon

            frame = tk.Frame(self.main_frame, bg="#2C2F33", padx=5, pady=5, relief="flat")
            frame.grid(row=row, column=col, padx=10, pady=5, sticky="w")

            logo_label = tk.Label(frame, image=instance_icon, bg="#2C2F33")
            logo_label.image = instance_icon
            logo_label.pack(padx=5)

            truncated_text = self.truncate_text(instance["name"], ("Arial", 10), MAX_TEXT_WIDTH)
            name_label = tk.Label(frame, text=truncated_text, font=("Arial", 10), fg="white",
                                  bg="#2C2F33", anchor="w", wraplength=MAX_TEXT_WIDTH)
            name_label.pack(padx=5, fill="x", expand=True)

            def on_instance_click(inst=instance):
                self.selected_instance = inst
                self.update_right_bar(inst)

            frame.bind("<Button-1>", lambda e, inst=instance: on_instance_click(inst))
            logo_label.bind("<Button-1>", lambda e, inst=instance: on_instance_click(inst))
            name_label.bind("<Button-1>", lambda e, inst=instance: on_instance_click(inst))

            col += 1
            if col >= num_columns:
                col = 0
                row += 1
                
    def load_accounts(self):
        accounts_json = json.loads(load_file("accounts.json"))
        
        self.options = []
        for acc in accounts_json["accounts"]:
            self.options.append(acc["name"])
        
        self.options.append("Add Account")

        self.images = {}
        for opt in self.options:
            if opt != "Add Account":
                r = requests.get(f"https://cdn.classicube.net/skin/{opt}.png")
                try:
                    img = Image.open(io.BytesIO(r.content))
                except IOError:
                    r = requests.get(f"https://Tycho10101.is-a.dev/Assets/char.png")
                    img = Image.open(io.BytesIO(r.content))
                width, height = img.size
                mult = width/64
                img2 = img.crop((40*mult, 8*mult, 48*mult, 16*mult)).convert().convert('RGBA')
                img = img.crop((8*mult, 8*mult, 16*mult, 16*mult)).convert("RGB")
                img.paste(img2, (0,0), img2) 
                self.images[opt] = ImageTk.PhotoImage(img.resize((30, 30), Image.Resampling.NEAREST))
        

    def open_add_instance(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Instance")
        add_window.geometry("300x250")
        add_window.configure(bg="#2C2F33")

        tk.Label(add_window, text="Instance Name:", bg="#2C2F33", fg="white").pack(pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.pack(pady=5)

        version_type = tk.StringVar(value="stable")
        versions_dropdown = ttk.Combobox(add_window, state="readonly")
        versions_dropdown["values"] = getVersions("stable")
        versions_dropdown.current(0)

        def update_versions():
            versions_dropdown["values"] = getVersions(version_type.get())
            versions_dropdown.current(0)

        stable_radio = tk.Radiobutton(add_window, text="Stable", variable=version_type, value="stable",
                                      command=update_versions, bg="#2C2F33", fg="white", selectcolor="#2C2F33")
        dev_radio = tk.Radiobutton(add_window, text="Dev", variable=version_type, value="dev",
                                   command=update_versions, bg="#2C2F33", fg="white", selectcolor="#2C2F33")

        stable_radio.pack()
        dev_radio.pack()
        versions_dropdown.pack(pady=5)

        def create_instance():
            name = name_entry.get().strip()
            version = versions_dropdown.get()
            if name and not instanceNameExists(name):
                makeInstance(name, version)
                add_window.destroy()
                self.load_instances()

        tk.Button(add_window, text="Create", command=create_instance, bg="#7289DA", fg="white").pack(pady=10)

    def select_option(self, option):
        if not option == "Add Account":
            if option in self.images:
                self.acc_switch_button.config(text=option, image=self.images[option], compound="left")
            else:
                self.acc_switch_button.config(text=option, image='', compound="left")
            accounts_json = json.loads(load_file("accounts.json"))
            accounts_json["Selected Account"] = option
            save_file("accounts.json", json.dumps(accounts_json))
        else:
            self.open_add_account()
        self.close_menu()

    def show_menu(self):
        self.close_menu()

        self.dropdown_window = tk.Toplevel(self.root)
        self.dropdown_window.overrideredirect(True)
        self.update_menu_position()

        for option in self.options:
            frame = tk.Frame(self.dropdown_window)
            frame.pack(fill="x")

            if option in self.images:
                img_label = tk.Label(frame, image=self.images[option], width=30, height=30)
                img_label.pack(side="left")

            opt_button = tk.Button(frame, text=option, command=lambda opt=option: self.select_option(opt), anchor="w")
            opt_button.pack(fill="x", expand=True)

        self.root.bind("<Configure>", self.update_menu_position)

    def update_menu_position(self, event=None):
        if self.dropdown_window:
            self.dropdown_window.geometry(f"150x{35*len(self.options)}+{self.acc_switch_button.winfo_rootx()}+{self.acc_switch_button.winfo_rooty() + self.acc_switch_button.winfo_height()}")

    def close_menu(self):
        if self.dropdown_window:
            self.dropdown_window.destroy()
            self.dropdown_window = None
            self.root.unbind("<Configure>")
            
    def open_add_account(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Account")
        add_window.geometry("300x250")
        add_window.configure(bg="#2C2F33")

        tk.Label(add_window, text="Username:", bg="#2C2F33", fg="white").pack(pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.pack(pady=5)
        
        tk.Label(add_window, text="Password:", bg="#2C2F33", fg="white").pack(pady=5)
        password_entry = tk.Entry(add_window, show="•")
        password_entry.pack(pady=5)
        
        status = tk.Label(add_window, text="", bg="#2C2F33", fg="red")
        status.pack(pady=5)

        def create_account():
            name = name_entry.get().strip()
            password = password_entry.get().strip()
            login = login_to_cc(name, password)
            if name and password and not username_exists(name) and login[0]:
                save_account(login[1], password)
                self.load_accounts()
                self.select_option(login[1])
                add_window.destroy()
            elif not name and not password:
                status.config(text = "No Username or Password")
            elif not name:
                status.config(text = "No Username")
            elif not password:
                status.config(text = "No Password")
            elif username_exists(name):
                status.config(text = "Account already exists")
            else:
                status.config(text = "Failed to login")
                
        tk.Button(add_window, text="Login", command=create_account, bg="#7289DA", fg="white").pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = LaunchiCubeApp(root)
    root.mainloop()  
