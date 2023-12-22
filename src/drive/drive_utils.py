import io

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


def all_drive(creds):
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list().execute()
    items = results.get('files', [])

    if not items:
        print("No files found")
        return
    return items


def download_file(creds, file_id):
    if file_id:
        service = build('drive', 'v3', credentials=creds)
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}")
        return file.getvalue()
