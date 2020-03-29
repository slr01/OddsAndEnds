#!/usr/bin/python3
#Script to web scrape mincraft server link, download and update minecraft server
#pip3 install requests beautifulsoup4 wget

import requests
from bs4 import BeautifulSoup
import wget
import subprocess

serverdir = "/home/minecraft"
URL = 'https://www.minecraft.net/en-us/download/server/'

try:
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    downloadURL = soup.find('a', {'aria-label':"mincraft version"}).get('href')
    version = soup.find('a', {'aria-label':"mincraft version"}).get_text()
except:
    print("Something went wrong. Did the URL or webpage recently change?")
else:
    print(f"Downloading {version}.")
    wget.download(downloadURL, version)
    print("\nDownload complete.")
    subprocess.run(["/etc/init.d/minecraft","stop"])
    subprocess.run(["rm",f"{serverdir}/minecraft_server.jar"])
    print("Old symlink removed.")
    subprocess.run(["ln","-s",f"{serverdir}/{version}",f"{serverdir}/minecraft_server.jar"])
    print("New symlink created.")
    subprocess.run(["/etc/init.d/minecraft","start"])
    print("Script complete.")