from requests import get

class installer_backend:
    def install():
        linkbase = "https://raw.githubusercontent.com/Tycho10101/LaunchiCube/refs/heads/main/"
        installer_backend.save_link_as_file(f"{linkbase}main.py", "main.py")
        installer_backend.save_link_as_file(f"{linkbase}updater.py", "updater.py")
        installer_backend.save_link_as_file(f"{linkbase}gui.py", "gui.py")
        installer_backend.save_link_as_file(f"{linkbase}utils.py", "utils.py")

    def save_link_as_file(link, filepath, by=False):
        r = get(link, timeout=60)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(r.text)
