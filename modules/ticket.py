from tickets_dao import Ticket_db


class Ticket():
    def __init__(self, ticket_id=int, customer_mail=str, question=str, thread_id = str, history = dict, product_tags=list, problem_tags=list, level=int, extra_bin=str):
        super().__init__()
        self.ticket_id = ticket_id
        self.customer_mail = customer_mail
        self.question = question
        self.history = history
        self.thread_id = thread_id
        self.product_tags = product_tags
        self.problem_tags = problem_tags
        self.level = level
        self.extra_bin = extra_bin


    def add_entry(self):
        ticketdb_instance = Ticket_db()
        ticketdb_instance.add_entry(self.ticket_id,
                                    self.customer_mail,
                                    self.question,
                                    self.product_tags,
                                    self.problem_tags,
                                    self.level,
                                    self.extra_bin)


    def escalate(self):
        pass

    #deleteticket, getforticket > tags, bin

ticket_instance = Ticket(1,
                         "shttybitty@gmail.com",
                         'Wie kann ich mein blank zurücksetzen?',
                         ['vibrator', 'elektrisch'],
                         ['wichsen'],
                         1,
                         'Zusätzliche Informationen hier')
ticket_instance.add_entry()

