import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# إعداد OAuth
def authenticate():
    gauth = GoogleAuth()

    # لو ملف الاعتماد مش موجود اعمل المصادقة
    if not os.path.exists("credentials.json"):
        gauth.LocalWebserverAuth()
    else:
        gauth.LoadCredentialsFile("credentials.json")
        if gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

    gauth.SaveCredentialsFile("credentials.json")
    return GoogleDrive(gauth)

# تحميل ملف من Google Drive (إن وجد)
def download_file(drive, filename):
    file_list = drive.ListFile({'q': f"title='{filename}' and trashed=false"}).GetList()
    if file_list:
        file_list[0].GetContentFile(filename)
        print(f"📥 Downloaded {filename}")
    else:
        print(f"⚠️ File {filename} not found on Drive")

# رفع/تحديث ملف إلى Google Drive
def upload_file(drive, filename):
    file_list = drive.ListFile({'q': f"title='{filename}' and trashed=false"}).GetList()
    if file_list:
        file = file_list[0]
        file.SetContentFile(filename)
        file.Upload()
        print(f"🔁 Updated {filename} on Drive")
    else:
        file = drive.CreateFile({'title': filename})
        file.SetContentFile(filename)
        file.Upload()
        print(f"🆕 Uploaded {filename} to Drive")
