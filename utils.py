from os.path import exists, splitext, join
from re import sub

def load_file(filename):
    if exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    return ""

def save_file(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)

def get_safe_unique_filename(directory, filename):
    filename = sub(r'[<>:"/\\|?*]', "_", filename).strip().replace(" ", "_")
    base, ext = splitext(filename)
    counter = 1
    new_filename = filename

    while exists(join(directory, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1

    return new_filename

def change_option(instance, option, value):
    f = load_file(f"instances/{instance}/options.txt")
    f = f.split("\n")
    where = None
    for i in range(len(f)):
        if f[i].startswith(f"{option}="):
            where = i
    
    if where == None:
        f.append(f"{option}={value}")
    else:
        f[where] = f"{option}={value}"
    save_file(f"instances/{instance}/options.txt", "\n".join(f))
    
def delete_option(instance, option):
    f = load_file(f"instances/{instance}/options.txt")
    f = f.split("\n")
    where = None
    for i in range(len(f)):
        if f[i].startswith(f"{option}="):
            where = i
    
    if not where == None:
        del f[where]
    
    save_file(f"instances/{instance}/options.txt", "\n".join(f))
