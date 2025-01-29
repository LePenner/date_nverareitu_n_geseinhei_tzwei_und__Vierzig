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
    print(os.name)
    # ready console for pretty output
    Console.clear()

    # det path
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # constants
    CREDENTIALS_JSON = "modules/functionals/credentials.json"
    TOKEN_JSON = "modules/functionals/token.json"
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
        service = build("gmail", "v1", credentials=creds)

        poll_rate = 10  # polling rate in seconds - use more or eaqual to 10 to stay in monthly 2 mil call limit
        Console.spinner_speed = 8  # 4 equals one rotation a second

        count = poll_rate * Console.spinner_speed  # start count on max to ease debuging

        while True:

            # every 10 seconds the count reaches max
            if count >= poll_rate * Console.spinner_speed:
                check_mails(service)
                count = 0

            time.sleep(poll_rate / Console.spinner_speed / 10)
            Console.spinner_spin()

            count += 1

    except HttpError as error:
        Console.status(f"Error: {error}")


if __name__ == "__main__":
    main()
