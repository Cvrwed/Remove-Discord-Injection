import os ; import shutil
import subprocess

os.system("cls")
path = os.getenv("localappdata")
discord_folder = "Discord"
index_file = "index.js"

replace_js = "module.exports = require('./core.asar');"
check_process = subprocess.check_output(["tasklist"]).decode("unicode_escape")

def RemoveInjection():
    global path
    global discord_folder
    for folder in os.listdir(path):
        if discord_folder in folder:
            discord_path = os.path.join(path, folder)
            print("Scanning...")
            check_file(discord_path)

def check_file(path):
    global replace_js
    global index_file
    discord = path.split("\\")[5]
    is_safe = False
    for folder in os.listdir(path):
        if "app-" in folder:
            app_path = os.path.join(path, folder, "modules")
            for archive in os.listdir(app_path):
                if "discord_desktop_core-" in archive:
                    core_path = os.path.join(app_path, archive, "discord_desktop_core", "index.js")
                    with open(core_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    if content.strip() == "module.exports = require('./core.asar');":
                        print(f"The content of {discord} is normal.")
                        is_safe = True
                        break
                    else:
                        replace_js = replace_js.format(discord)
                        if not os.path.exists('Danger'):
                            os.makedirs('Danger')
                        shutil.copy(core_path, "Danger/Infected_index.js")
                        print(f"The content of {discord} is suspicious.")
                        print("Replacing index.js...")
                        with open(core_path, "w", encoding="utf-8") as f:
                            f.write(replace_js)
                            print(f"{discord} is now safe. \nReloading {discord}...")
                            Reload(discord)
            if is_safe:
                break

def Reload(discord):
    if discord in check_process:
        subprocess.call(f"taskkill /IM {discord}.exe /F")
        while discord in check_process:
            continue
    else:pass
    print(f"Starting {discord}...")
    subprocess.call(f"{os.path.join(path, discord_folder)}\\Update.exe --processStart {discord}.exe")

RemoveStealer()
