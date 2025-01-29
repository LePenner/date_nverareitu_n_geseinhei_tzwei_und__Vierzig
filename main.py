import os
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# own imports
from modules.bot import Bot
from modules.functionals.sending_messages import send_mail
from modules.functionals.check_messages import check_mails
from modules.console import Console


def main():

    Console.clear()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    credentials_json = "modules/functionals/credentials.json"
    token_json = "modules/functionals/token.json"

    SCOPES = ["https://mail.google.com/"]

    creds = None
    if os.path.exists(token_json):
        creds = Credentials.from_authorized_user_file(token_json, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_json, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(token_json, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)

        poll_rate = 10  # polling rate in seconds - use more or eaqual to 10
        Console.spinner_speed = 8

        count = poll_rate * Console.spinner_speed

        while True:

            Console.spinner_spin()

            if count >= poll_rate * Console.spinner_speed:
                check_mails(service)
                count = 0

            time.sleep(poll_rate / Console.spinner_speed / 10)
            count += 1

    except HttpError as error:
        Console.status(f"Ein Fehler ist aufgetreten: {error}")


if __name__ == "__main__":
    main()
