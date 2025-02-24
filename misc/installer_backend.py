from utils import save_link_as_file

class installer_backend:
    def install():
        linkbase = "https://raw.githubusercontent.com/Tycho10101/LaunchiCube/refs/heads/main/"
        save_link_as_file(f"{linkbase}main.py", "main.py")
        save_link_as_file(f"{linkbase}updater.py", "updater.py")
        save_link_as_file(f"{linkbase}gui.py", "gui.py")
        save_link_as_file(f"{linkbase}utils.py", "utils.py")
