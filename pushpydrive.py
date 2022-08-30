from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()           
drive = GoogleDrive(gauth)  


gauth.LoadCredentialsFile("creds.txt")
file_to_upload = "final_sorted_list.json"
gfile = drive.CreateFile({'parents': [{'id': '1gL99YWdA0vTawbvGs8nGDGww2fc1X4_v'}]})
gfile.SetContentFile(file_to_upload)
gfile.Upload()
gauth.SaveCredentialsFile("creds.txt")
