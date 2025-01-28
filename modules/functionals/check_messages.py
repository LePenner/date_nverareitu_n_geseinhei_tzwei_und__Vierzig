import os
import time
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def check_mails(service):

    try:

        # search for mails with lable unred
        results = service.users().messages().list(
            userId="me", labelIds=["INBOX"], q="is:unread").execute()
        messages = results.get("messages", [])

        if not messages:
            print('fetching')

        # mails found
        else:
            print(f"{len(messages)} new mails")

            for message in messages:

                # get full message (other is just id)
                message = service.users().messages().get(
                    userId="me", id=message.get('id'), format="full").execute()

                headers = message["payload"]["headers"]
                subject = next(
                    (header["value"] for header in headers if header["name"] == "Subject"), "No Subject")
                sender = next(
                    (header["value"] for header in headers if header["name"] == "From"), "Unknown Sender")

                # Extract message body (plain text or HTML)
                body = None
                parts = message["payload"].get("parts", [])
                for part in parts:
                    if part["mimeType"] == "text/plain":
                        body = base64.urlsafe_b64decode(
                            part["body"]["data"]).decode("utf-8")
                        break
                    elif part["mimeType"] == "text/html":  # Optional: for HTML emails
                        body = base64.urlsafe_b64decode(
                            part["body"]["data"]).decode("utf-8")
                        break

                try:
                    # mark message as read
                    service.users().messages().modify(
                        userId="me",
                        id=message.get('id'),
                        body={"removeLabelIds": ["UNREAD"]}
                    ).execute()

                    print(f"Message {message.get('text')
                                     } handled")

                    data = {
                        'mail': {
                            'subject': subject,
                            'sender': sender,
                            'body': body
                        },
                        'thread_id': message.get('threadId')
                    }
                    return data

                except Exception as e:
                    print(f"Failed to mark message as read: {e}")

    except Exception as e:
        print(f"Fehler beim Abrufen neuer E-Mails: {e}")
