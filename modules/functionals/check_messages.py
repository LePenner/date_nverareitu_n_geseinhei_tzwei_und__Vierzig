import base64

from modules.bot import Bot
from modules.console import Console


def check_mails(service):

    try:

        # search for mails with lable unred
        results = service.users().messages().list(
            userId="me", labelIds=["INBOX"], q="is:unread").execute()
        messages = results.get("messages", [])

        if not messages:
            Console.status('fetching')

        # mails found
        else:
            Console.status(f"{len(messages)} new mails")

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

                if not parts:

                    try:
                        body = base64.urlsafe_b64decode(
                            message['payload']['body']['data']).decode("utf-8")
                    except Exception as e:
                        Console.status(f"Failed to read message: {e}")
                        break

                try:
                    # mark message as read
                    service.users().messages().modify(
                        userId="me",
                        id=message.get('id'),
                        body={"removeLabelIds": ["UNREAD"]}
                    ).execute()

                    Console.status(f"Message {message.get('id')
                                              } handled")

                    if "<" in sender:
                        email = sender.split("<")[1].strip(">")
                    else:
                        email = sender

                    data = {
                        'mail': {
                            'subject': subject,
                            'sender': sender,
                            'body': body
                        },
                        'thread_id': message.get('threadId'),
                        'email': email
                    }

                    if data:
                        Bot.input(data)

                except Exception as e:
                    Console.status(f"Failed to mark message as read: {e}")

    except Exception as e:
        Console.status(f"Fehler beim Abrufen neuer E-Mails: {e}")
