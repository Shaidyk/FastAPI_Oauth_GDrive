import json
import os.path
import sys
from json import JSONDecodeError

import fastapi
from dotenv import load_dotenv
from google.auth.transport import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

CLIENT_ID = os.environ.get('CLIENT_ID', None)
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', None)

JWT_SECRET = os.environ.get('JWT_SECRET')
MANAGER_SECRET = os.environ.get('MANAGER_SECRET')

DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/docs',
]


def request_creds(user_email):
    creds = None
    if os.path.exists('credentials/creds.json'):
        flow = InstalledAppFlow.from_client_secrets_file('credentials/creds.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open(f'user_creds/{user_email}.json', 'w') as token:
            token.write(creds.to_json())
        try:
            return Credentials.from_authorized_user_file(f'user_creds/{user_email}.json', SCOPES)
        except JSONDecodeError:
            pass
    else:
        print("Credentials not present")
        sys.exit(1)


def get_creds(user_email):
    if os.path.exists(f'user_creds/{user_email}.json'):
        creds = Credentials.from_authorized_user_file(f'user_creds/{user_email}.json', SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return creds
    return request_creds(user_email)
