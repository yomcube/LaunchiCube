from base64 import b64encode
import json
import os
from os.path import exists, splitext, join
from re import sub
from requests import Session
from sys import platform

PLAT_WIN = platform == 'win32' or platform == 'cygwin'
PLAT_NIX = platform == 'linux'
PLAT_MAC = platform == 'darwin'

def load_file(filename):
    if exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    return ""

def save_file(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)

def get_safe_unique_filename(directory, filename):
    filename = sub(r'[<>:"/\\|?*]', "_", filename).strip().replace(" ", "_")
    base, ext = splitext(filename)
    counter = 1
    new_filename = filename

    while exists(join(directory, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1

    return new_filename

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


## Instance utils ##
if PLAT_WIN:
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
                return b64encode(encrypted_bytes).decode("utf-8")
            else:
                raise RuntimeError(f"Encryption failed. Error Code: {ctypes.windll.kernel32.GetLastError()}")
    finally:
        pass

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
    session = Session()
    r = session.get("https://www.classicube.net/api/login/")
    myobj = {"username": username, "password": password, "token": r.json()["token"]}
    x = session.post("https://www.classicube.net/api/login/", data=myobj)
    return [x.json()["authenticated"],x.json()["username"]]
