from utils import get, save_link_as_file

class installer_backend:
    def install():
        linkbase = "https://raw.githubusercontent.com/Tycho10101/LaunchiCube/refs/heads/main/"
        utils.save_link_as_file(f"{linkbase}main.py", "main.py")
        utils.save_link_as_file(f"{linkbase}updater.py", "updater.py")
        utils.save_link_as_file(f"{linkbase}gui.py", "gui.py")
        utils.save_link_as_file(f"{linkbase}utils.py", "utils.py")
