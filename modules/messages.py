import base64

from email.message import EmailMessage
from googleapiclient.errors import HttpError

# own imports
from modules.console import Console

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

    except HttpError as error:
        Console.status(f"An error occurred: {error}")
        send_message = None
    return send_message
