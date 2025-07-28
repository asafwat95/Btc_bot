from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def authenticate_drive():
    # حفظ ملف credentials.json لو مش موجود
    with open("client_secrets.json", "w") as f:
        f.write(os.environ["GDRIVE_CLIENT_SECRETS"])

    gauth = GoogleAuth()
    gauth.LoadClientConfigFile("client_secrets.json")

    # لأول مرة لازم نسجل يدويًا
    gauth.LocalWebserverAuth()  # يفتح متصفح لتسجيل الدخول
    return GoogleDrive(gauth)

def upload_file(drive, local_file, remote_name):
    file_list = drive.ListFile({'q': f"title='{remote_name}' and trashed=false"}).GetList()
    
    if file_list:
        file = file_list[0]
        file.SetContentFile(local_file)
        file.Upload()
        print(f"🔁 Updated {remote_name} on Drive")
    else:
        file = drive.CreateFile({'title': remote_name})
        file.SetContentFile(local_file)
        file.Upload()
        print(f"✅ Uploaded new file {remote_name} to Drive")
