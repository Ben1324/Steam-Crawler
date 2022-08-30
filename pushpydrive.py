from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

gauth = GoogleAuth()           
drive = GoogleDrive(gauth)  

game_ID = os.getenv("STEAM_ID")
if game_ID == None:
    game_ID = 1044720

gauth.LoadCredentialsFile("creds.txt")
absolute_path = os.path.abspath(".")
for filename in os.listdir(absolute_path):
    if filename.endswith(f"{game_ID}"):
        gfile = drive.CreateFile({'parents': [{'id': '1gL99YWdA0vTawbvGs8nGDGww2fc1X4_v'}]})
        gfile.SetContentFile(filename)
        gfile.Upload()
        gauth.SaveCredentialsFile("creds.txt")
