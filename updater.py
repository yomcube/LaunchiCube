import io
import json
import os
import sys
from tarfile import TarFile
from zipfile import ZipFile

import utils

def update_clients():
    r = utils.get("https://cdn.classicube.net/client/builds.json")
    f = json.loads(utils.load_file("clients/index.json"))
    
    if not json.loads(r.text)["release_version"] == f["release_ver"]:
        print("Downloading Latest Release Version")
        f["release_ver"] = json.loads(r.text)["release_version"]
        utils.save_file("clients/index.json", json.dumps(f))
        download_release()
    
    if not json.loads(r.text)["latest_ts"] == f["dev_ver"]:
        print("Downloading Latest Dev Version")
        f["dev_ver"] = json.loads(r.text)["latest_ts"]
        utils.save_file("clients/index.json", json.dumps(f))
        download_dev()
         
def download_release():
    bits = '64' if sys.maxsize > 2**32 else '32'
    
    if utils.PLAT_WIN:
        url = f"https://cdn.classicube.net/client/release/win{bits}/ClassiCube.zip"
        r = utils.get(url)


        with ZipFile(io.BytesIO(r.content)) as z:
            z.extract("ClassiCube/ClassiCube.exe", path="clients/temp/")
            z.close()
        if os.path.isfile("clients/Latest Stable Version.exe"):
            os.remove("clients/Latest Stable Version.exe")
        os.rename("clients/temp/ClassiCube/ClassiCube.exe", "clients/Latest Stable Version.exe")
        os.rmdir("clients/temp/ClassiCube")
        os.rmdir("clients/temp/")
    
    else:
        cc_os = 'osx' if utils.PLAT_MAC else 'nix'
        url = f"https://cdn.classicube.net/client/release/{cc_os}{bits}/ClassiCube.tar.gz"
        r = utils.get(url)
            
        with TarFile.open(fileobj=io.BytesIO(r.content)) as t:
            t.extract("ClassiCube/ClassiCube", path="clients/temp/") # Gives a deprecation warning
            t.close()
        if os.path.isfile("clients/Latest Stable Version"):
            os.remove("clients/Latest Stable Version")
        os.rename("clients/temp/ClassiCube/ClassiCube", "clients/Latest Stable Version")
        os.rmdir("clients/temp/ClassiCube")
        os.rmdir("clients/temp/")
            
def download_dev():
    bits = '64' if sys.maxsize > 2**32 else '32'
    ext = '.exe' if utils.PLAT_WIN else ''
    base = 'https://nightly.link/ClassiCube/ClassiCube/workflows/build_'
    r, cc_os = None, None
    if utils.PLAT_WIN:
        r = utils.get(f"{base}windows/master/ClassiCube-Win{bits}-Direct3D9.exe.zip")
        cc_os = 'w'
    elif utils.PLAT_MAC:
        r = utils.get(f"{base}mac{bits}/master/ClassiCube-mac{bits}-OpenGL.zip")
        cc_os = 'mac'
    elif utils.PLAT_NIX:
        r = utils.get(f"{base}linux/master/ClassiCube-Linux{bits}-OpenGL.zip")
        cc_os = 'nix'
        
    with ZipFile(io.BytesIO(r.content)) as z:
        z.extractall(path="clients/temp/")
        z.close()
    
    if os.path.isfile(f"clients/Latest Dev Version{ext}"):
        os.remove(f"clients/Latest Dev Version{ext}")
    filename = f"cc-{cc_os}{bits}-{'d3d9' if utils.PLAT_WIN else 'gl1'}{ext}"
    os.rename(f"clients/temp/{filename}", f"clients/Latest Dev Version{ext}")
    os.rmdir("clients/temp/")
