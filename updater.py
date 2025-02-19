import io
import json
import os
import sys
from tarfile import TarFile
from zipfile import ZipFile

from requests import get

from utils import *

class Updater:
    def update_clients():
        r = get("https://cdn.classicube.net/client/builds.json", timeout=60)
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
        bits = '64' if sys.maxsize > 2**32 else '32'
        base = "https://cdn.classicube.net/client/release"
        if PLAT_WIN:
            url = f"{base}/win{bits}/ClassiCube.zip"
            r = get(url, timeout=60)


            z = ZipFile(io.BytesIO(r.content))
            z.extract("ClassiCube/ClassiCube.exe", path="clients/temp/")
            if os.path.isfile("clients/Latest Stable Version.exe"):
                os.remove("clients/Latest Stable Version.exe")
            os.rename("clients/temp/ClassiCube/ClassiCube.exe", "clients/Latest Stable Version.exe")
            z.close()
        
        else:
            cc_os = 'osx' if PLAT_MAC else 'nix'
            url = f"{base}/{cc_os}{bits}/ClassiCube.tar.gz"
            r = get(url, timeout=60)
                
            t = TarFile.open(fileobj=io.BytesIO(r.content))
            t.extract("ClassiCube/ClassiCube", path="clients/temp/") # Gives a deprecation warning
            if os.path.isfile("clients/Latest Stable Version"):
                os.remove("clients/Latest Stable Version")
            os.rename("clients/temp/ClassiCube/ClassiCube", "clients/Latest Stable Version")
            t.close()
        
        os.rmdir("clients/temp/ClassiCube")
        os.rmdir("clients/temp/")
                
    def download_dev():
        bits = '64' if sys.maxsize > 2**32 else '32'
        ext = '.exe' if PLAT_WIN else ''
        base = "https://nightly.link/ClassiCube/ClassiCube/workflows"
        if PLAT_WIN:
            r = get(f"{base}/build_windows/master/ClassiCube-Win{bits}-Direct3D9.exe.zip")
            cc_os = 'win'
        elif PLAT_MAC:
            r = get(f"{base}/build_mac{bits}/master/ClassiCube-mac{bits}-OpenGL.zip")
            cc_os = 'mac'
        elif PLAT_NIX:
            r = get(f"{base}/build_linux/master/ClassiCube-Linux{bits}-OpenGL.zip")
            cc_os = 'nix'
            
        z = ZipFile(io.BytesIO(r.content))
        z.extractall(path="clients/temp/")
        if os.path.isfile(f"clients/Latest Dev Version{ext}"):
            os.remove(f"clients/Latest Dev Version{ext}")
        filename = f"cc-{cc_os}{bits}-{'d3d9' if PLAT_WIN else 'gl1'}{ext}"
        os.rename(f"clients/temp/{filename}", f"clients/Latest Dev Version{ext}")
        z.close()
        os.rmdir("clients/temp/")
