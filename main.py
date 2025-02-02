import os
import time
import atexit

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# own imports
from modules.messages import check_mails
from modules.console import Console


#########################################################
# PLEASE LOG IN WITH bugland.botbob@gmail.com !!!!!!!!! #
#########################################################


def main():

    # ready console for pretty output
    if os.name == 'nt':
        os.system('cls')
        Console.default()
    elif os.name == 'posix':
        os.system('clear')
        Console.default()

    # det path
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # file paths
    CREDENTIALS_JSON = "modules/functionals/credentials.json"
    TOKEN_JSON = "modules/functionals/token.json"
    TAGS_JSON = "modules/functionals/tags.json"

    # If modifying these scopes, delete the file token.json.
    # https://mail.google.com gives perms do delete, read and write mails
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
    except HttpError as error:
        Console.status(f"Error while building service: {error}")

    PATHS = {'credentials': CREDENTIALS_JSON,
             'token': TOKEN_JSON,
             'tags': TAGS_JSON}

    # polling rate in seconds
    poll_rate = 10
    # use more or eaqual to 10 to stay in monthly 2 mil call limit
    # absolute limit: 1

    spinner_speed = 8

    # keep spinner speed constant at different poll rates
    Console.spinner_speed = spinner_speed*poll_rate/10

    # set count to max at startup, to process all backups immediately
    count = poll_rate * Console.spinner_speed

    # main loop
    while True:

        if count >= poll_rate * Console.spinner_speed:
            check_mails(SERVICE, PATHS)
            count = 0

        time.sleep(poll_rate / Console.spinner_speed / 10)
        Console.spinner_spin()

        count += 1


def at_exit():
    os.system('log.txt')


atexit.register(at_exit)

if __name__ == "__main__":
    main()
