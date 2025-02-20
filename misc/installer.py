import os
from requests import get

from installer_backend import installer_backend

def save_link_as_file(link, filepath):
    r = get(link, timeout=60)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(r.text)

linkbase = "https://raw.githubusercontent.com/Tycho10101/LaunchiCube/refs/heads/main/"
save_link_as_file(f"{linkbase}misc/installer_backend.py", "installer_backend.py")
installer_backend.install()
os.remove("installer_backend.py")
os.remove("installer.py")
