import os
import base64

from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from modules.console import Console


#########################################################
# PLEASE LOG IN WITH bugland.botbob@gmail.com !!!!!!!!! #
#########################################################


def send_mail(SERVICE, adress, header, content):

    try:
        message = EmailMessage()

        message.set_content(content)

        message["To"] = adress
        message["From"] = "bugland.botbob@gmail.com"
        message["Subject"] = header

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}

        send_message = (
            SERVICE.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        Console.status(f'Message sent. Id: {send_message["id"]}')
    except HttpError as error:
        Console.status(f"An error occurred: {error}")
        send_message = None
    return send_message
