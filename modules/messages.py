import base64

from email.message import EmailMessage
from googleapiclient.errors import HttpError

# own imports
from modules.console import Console
from modules.bot import Bot


def check_mails(SERVICE, PATHS):

    try:

        # search for mails with lable unred
        results = SERVICE.users().messages().list(
            userId="me", labelIds=["INBOX"], q="is:unread").execute()
        messages = results.get("messages", [])

        if not messages:
            Console.status('fetching')

        # on mails found
        else:
            Console.status(f"{len(messages)} new mails")

            for indx, message in enumerate(messages, start=1):

                Console.status(f'processing message {indx}/{len(messages)}')

                # get full message (other is just id)
                message = SERVICE.users().messages().get(
                    userId="me", id=message.get('id'), format="full").execute()

                # header and sender
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

                # for unknown email structures:
                if not parts:

                    try:
                        body = base64.urlsafe_b64decode(
                            message['payload']['body']['data']).decode("utf-8")
                    except Exception as e:
                        Console.status(f"Failed to read message: {e}")
                        break

                # seperate email from sender
                if "<" in sender:
                    email = sender.split("<")[1].strip(">")
                else:
                    email = sender
                name = email.split("@")[0]
                # format needed data
                data = {
                    'mail': {
                        'subject': subject,
                        'sender': sender,
                        'body': body
                    },
                    'thread_id': message.get('threadId'),
                    'email': email,
                    'name': name,
                    'service': SERVICE,
                    'paths': PATHS,
                    'message_id': message.get('id')
                }

                Console.log(f'{message.get('id')}, {data['message_id']}')

                if data:

                    ################################################
                    #                 start the bot                #
                    ################################################

                    Bot.input(data)

    except Exception as e:
        Console.status(f"processing failed: {e}")


def mark_as_read(SERVICE, message_id):

    try:
        # mark message as read
        SERVICE.users().messages().modify(
            userId="me",
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

        Console.status(
            f"Message {message_id} marked as read")

    except Exception as e:
        Console.status(f"Failed to mark message as read: {e}")


def send_mail(data, content):

    adress = data['email']
    subject = data['mail']['subject']
    thread_id = data['thread_id']
    SERVICE = data['service']

    try:
        message = EmailMessage()

        message.set_content(content)

        message["To"] = adress
        message["From"] = "bugland.botbob@gmail.com"
        message["Subject"] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message,
                          "threadId": thread_id}

        send_message = (
            SERVICE.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )

        Console.status(f'Message sent. Id: {send_message["id"]} Thread Id: {
                       send_message['threadId']}')
        Console.status('Request Handled')

    except HttpError as error:
        Console.status(f"An error occurred: {error}")
        send_message = None
    return send_message
