import io
import json
import requests
import os
import sys
from tarfile import TarFile
from zipfile import ZipFile

from utils import *

class Updater:
    def update_clients():
        r = requests.get("https://cdn.classicube.net/client/builds.json")
        f = json.loads(load_file("clients/index.json"))
        
        if not json.loads(r.text)["release_version"] == f["release_ver"]:
            print("Downloading Latest Release Version")
            f["release_ver"] = json.loads(r.text)["release_version"]
            save_file("clients/index.json", json.dumps(f))
            Updater.download_release()
        
        if not json.loads(r.text)["latest_ts"] == f["dev_ver"]:
            print("Downloading Latest Dev Version")
            f["dev_ver"] = json.loads(r.text)["latest_ts"]
            save_file("clients/index.json", json.dumps(f))
            Updater.download_dev()
             
    def download_release():
        is_64bit = sys.maxsize > 2**32
        
        if PLAT_WIN:
            url = f"https://cdn.classicube.net/client/release/win{'64' if is_64bit else '32'}/ClassiCube.zip"
            r = requests.get(url)


            z = ZipFile(io.BytesIO(r.content))
            z.extract("ClassiCube/ClassiCube.exe", path="clients/temp/")
            if os.path.isfile("clients/Latest Stable Version.exe"):
                os.remove("clients/Latest Stable Version.exe")
            os.rename("clients/temp/ClassiCube/ClassiCube.exe", "clients/Latest Stable Version.exe")
            z.close()
            os.rmdir("clients/temp/ClassiCube")
            os.rmdir("clients/temp/")
        
        else:
            cc_os = 'osx' if PLAT_MAC else 'nix'
            url = f"https://cdn.classicube.net/client/release/{cc_os}{'64' if is_64bit else '32'}/ClassiCube.tar.gz"
            r = requests.get(url)
                
            t = TarFile.open(fileobj=io.BytesIO(r.content))
            t.extract("ClassiCube/ClassiCube", path="clients/temp/") # Gives a deprecation warning
            if os.path.isfile("clients/Latest Stable Version"):
                os.remove("clients/Latest Stable Version")
            os.rename("clients/temp/ClassiCube/ClassiCube", "clients/Latest Stable Version")
            t.close()
            os.rmdir("clients/temp/ClassiCube")
            os.rmdir("clients/temp/")
                
    def download_dev():
        is_64bit = sys.maxsize > 2**32
        ext = '.exe' if PLAT_WIN else ''
        if PLAT_WIN:
            r = requests.get(f"https://nightly.link/ClassiCube/ClassiCube/workflows/build_windows/master/ClassiCube-Win{'64' if is_64bit else '32'}-Direct3D9.exe.zip")
            cc_os = 'win'
        elif PLAT_MAC:
            r = requests.get(f"https://nightly.link/ClassiCube/ClassiCube/workflows/build_mac{'64' if is_64bit else '32'}/master/ClassiCube-mac{'64' if is_64bit else '32'}-OpenGL.zip")
            cc_os = 'mac'
        elif PLAT_NIX:
            r = requests.get(f"https://nightly.link/ClassiCube/ClassiCube/workflows/build_linux/master/ClassiCube-Linux{'64' if is_64bit else '32'}-OpenGL.zip")
            cc_os = 'nix'
            
        z = ZipFile(io.BytesIO(r.content))
        z.extractall(path="clients/temp/")
        if os.path.isfile(f"clients/Latest Dev Version{ext}"):
            os.remove(f"clients/Latest Dev Version{ext}")
        filename = f"cc-{cc_os}{'64' if is_64bit else '32'}-{'d3d9' if PLAT_WIN else 'gl1'}"
        os.rename("clients/temp/cc-w64-d3d9.exe", f"clients/Latest Dev Version{ext}")
        z.close()
        os.rmdir("clients/temp/")
