from modules.bot import Bot
import os
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# own imports
from modules.console import Console


def test_mail():
    CREDENTIALS_JSON = "modules/functionals/credentials.json"
    TOKEN_JSON = "modules/functionals/token.json"
    TAGS_JSON = "modules/functionals/tags.json"

    PATHS = {'credentials': CREDENTIALS_JSON,
             'token': TOKEN_JSON,
             'tags': TAGS_JSON}

    SCOPES = ["https://mail.google.com/"]

    # check for gmail token, if not found ask user to log in and create token
    creds = None
    if os.path.exists(TOKEN_JSON):
        creds = Credentials.from_authorized_user_file(TOKEN_JSON, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_JSON, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_JSON, "w") as token:
            token.write(creds.to_json())

    try:
        SERVICE = build("gmail", "v1", credentials=creds)
        PATHS = {'credentials': CREDENTIALS_JSON,
                 'token': TOKEN_JSON,
                 'tags': TAGS_JSON}
    except Exception as e:
        Console.log(f'Test failed {e}')

    email = "erikblunk42@gmail.com"
    complaint = "ich complaine"

    data = {
        'mail': {'subject': 'Test',
                 'sender': 'Test',
                 'body': 'Hi I need help with my window fly, its not getting off the window!'
                 },
        'thread_id': "",
        'email': email,
        'name': 'Erik Blunk',
        'service': SERVICE,
        'paths': PATHS
    }

    Bot.input(data)
