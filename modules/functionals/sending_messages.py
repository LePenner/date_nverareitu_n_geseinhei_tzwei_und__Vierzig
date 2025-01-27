import os
import base64

from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# https://mail.google.com gives perms do delete, read and write mails
SCOPES = ["https://mail.google.com/"]

########################################################
# PLEASE LOG IN WITH bugland.botbob@gmil.com !!!!!!!!! #
########################################################

def send_mail(adress, header, content):

  credentials_json = "modules/functionals/credentials.json"
  token_json = "modules/functionals/token.json"
  
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(token_json):
    creds = Credentials.from_authorized_user_file(token_json, SCOPES)

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          credentials_json, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(token_json, "w") as token:
      token.write(creds.to_json())

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    # ----------------------------- message content <--> text here ----------------------------- #
    message.set_content(content)

    message["To"] = adress
    message["From"] = "bugland.botbob@gmail.com"
    message["Subject"] = header

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message