from modules.ticket import Ticket_db

response = 'Subject: Regarding your recent BUGLAND Ltd. Support Request (Ticket #c71fc5d6-abd1-48e0-bb93-4549fe1d1082)\n\nDear erikblunk42,\n\nThank you for contacting BUGLAND Ltd. regarding the issues you experienced with your Cleanbug and Gardenbeetle. We appreciate you bringing these matters to our attention and value your business.\n\nWe understand your frustration with the Cleanbugs reduced suction power and the Gardenbeetles unexpected pursuit of your dog. Were also looking into the reported weakening battery in your Gardenbeetle.  These issues are being investigated by our specialist team.\n\nA member of our support team will be in touch with you within 24-48 hours to discuss these problems in more detail and to find a suitable solution. This may involve troubleshooting steps, a repair, or a replacement depending on the nature of the faults.  We will strive to resolve this for you as quickly and efficiently as possible.\n\nWe greatly appreciate your patience and understanding as we work to resolve these issues.  Thank you again for choosing BUGLAND Ltd.\n\nSincerely,\n\nThe BUGLAND Ltd. Customer Support Team\n'
UUID = "126384LSFEH"
email = "thilo.butt@gmail.com"
complaint = "ich complaine"

data = {
    'mail': {
    },
    'thread_id': "message.get('threadId')",
    'email': "email",
    'name': "name",
    'service': "SERVICE",
    'paths': "PATHS"
}

ticket_instance = Ticket_db()
ticket_instance.create_ticket(UUID, email, complaint, response, processedcomplaint, data)