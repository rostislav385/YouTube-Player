import os
import requests
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import shutil
import ctypes
import sys
def is_admin():
    pass
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def download_suc():
    try:
        print("Files were downloaded. Try to replace them, please wait...")
        source = './update/Rotipy.exe'
        destination = './Rotipy.exe'

        # Перемещение файла с заменой
        shutil.move(source, destination)

        os.system('cls')
        input("If you see this message the app is updated, press any key to close:")
    except:
        print(e)

if is_admin():
    print("Hello THERE")
    print("This is 'Rotipy' updater, it looks like the Version of the app is not the last one")
    print("Please confirm the installation of the new Version")
    print("WARNING: You are not allowed to use app, if it is not updated")

    a = input("Press '+' to confirm and  '-' to cancel update:")
    if a == "+":
        print("Wait, app will be updated...")
        print("Search for files...")
        dropbox_file_url = "https://www.dropbox.com/scl/fi/5pc61di1ey5o3sc6cs61c/Rotipy.exe?rlkey=1mnwhkg4qb7xwksvprtidqt6x&st=dc05s6ve&dl=1"

        # Путь для сохранения скачанного файла
        save_path = "./update/Rotipy.exe"

        # Скачивание файла
        response = requests.get(dropbox_file_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print("File successfully downloaded and saved as:", save_path)
        else:
            print("Error downloading file. Status code:", response.status_code)

            
        os.system('cls')
        download_suc()
    else:
        print("Installation is canceled :(")
        input("Press any key to close program:")
else:
    # Если не запущен с правами администратора, повторно запускаем с правами администратора
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()
