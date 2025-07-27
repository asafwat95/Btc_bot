# drive_util.py
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def authenticate():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # سيطلب منك تسجيل الدخول أول مرة
    return GoogleDrive(gauth)

def download_file(drive, filename):
    file_list = drive.ListFile({'q': f"title='{filename}'"}).GetList()
    if file_list:
        file_list[0].GetContentFile(filename)

def upload_file(drive, filename):
    file_list = drive.ListFile({'q': f"title='{filename}'"}).GetList()
    if file_list:
        file = file_list[0]
    else:
        file = drive.CreateFile({'title': filename})
    file.SetContentFile(filename)
    file.Upload()
