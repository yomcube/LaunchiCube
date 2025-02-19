from base64 import b64encode
import json
import os
from os.path import exists, splitext, join
from re import sub
from sys import platform

from requests import Session

PLAT_WIN = platform in ('win32' or 'cygwin')
PLAT_NIX = platform == 'linux'
PLAT_MAC = platform == 'darwin'

def load_file(filename):
    """If the given file exists, returns the contents. Otherwise returns an empty string."""
    if exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    return ""

def save_file(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)

def get_safe_unique_filename(directory, filename):
    """Returns an NTFS safe filename."""
    filename = sub(r'[<>:"/\\|?*]', "_", filename).strip().replace(" ", "_")
    base, ext = splitext(filename)
    counter = 1
    new_filename = filename

    while exists(join(directory, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1

    return new_filename

def search_option(lines, instance, option) -> int or None:
    """Internal function. Returns the line index of an option in `options.txt`, or `None` if that option does not exist."""
    where = None
    for idx, val in enumerate(lines):
        if val.startswith(f"{option}="):
            where = idx
    return where

def change_option(instance, option, value):
    """Changes an option in `options.txt`. Returns nothing."""
    f = load_file(f"instances/{instance}/options.txt")
    lines = f.split("\n")
    where = search_option(lines, instance, option)
    
    if where is None:
        f.append(f"{option}={value}")
    else:
        f[where] = f"{option}={value}"
    save_file(f"instances/{instance}/options.txt", "\n".join(f))
    
def delete_option(instance, option):
    """Deletes an option in `options.txt`. Returns nothing."""
    f = load_file(f"instances/{instance}/options.txt")
    lines = f.split("\n")
    where = search_option(lines, instance, option)
    
    if not where is None:
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
    url = "https://www.classicube.net/api/login/"
    r = session.get(url, timeout=60)
    myobj = {"username": username, "password": password, "token": r.json()["token"]}
    x = session.post(url, data=myobj).json()
    return [ x["authenticated"], x["username"] ]
