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
        with open(filepath, f"w{'b' if by else ''}") as f:
            f.write(r.content if by else r.text)
