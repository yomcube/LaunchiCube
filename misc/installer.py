import os
from requests import get

from installer_backend import installer_backend

def save_link_as_file(link, filepath, by=False):
    r = get(link, timeout=60)
    with open(filepath, f"w{'b' if by else ''}") as f:
        f.write(r.content if by else r.text)

linkbase = "https://raw.githubusercontent.com/Tycho10101/LaunchiCube/refs/heads/main/"
save_link_as_file(f"{linkbase}misc/installer_backend.py", "installer_backend.py")
installer_backend.install()
os.remove("installer_backend.py")
os.remove("installer.py")
