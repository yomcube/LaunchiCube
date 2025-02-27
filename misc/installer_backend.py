import requests

def save_link_as_file(link, filepath):
    import requests
    r = requests.get(link)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(r.text)
        
def install():
    linkbase = "https://raw.githubusercontent.com/Tycho10101/LaunchiCube/refs/heads/main/"
    save_link_as_file(f"{linkbase}main.py", "main.py")
    save_link_as_file(f"{linkbase}updater.py", "updater.py")
    save_link_as_file(f"{linkbase}gui.py", "gui.py")
    save_link_as_file(f"{linkbase}utils.py", "utils.py")
