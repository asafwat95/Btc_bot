from google_auth_oauthlib.flow import InstalledAppFlow

# السماح بالوصول إلى Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)

    auth_url, _ = flow.authorization_url(prompt='consent')
    print("🔗 افتح الرابط التالي لتفويض التطبيق:\n")
    print(auth_url)

if __name__ == '__main__':
    main()
