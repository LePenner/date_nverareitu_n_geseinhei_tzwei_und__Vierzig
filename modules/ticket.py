import sqlite3

class Ticket_db():
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("modules/functionals/tickets.db")
        self.cur = self.con.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id INTEGER,
                customer_mail TEXT,
                question TEXT,
                history TEXT,
                thread_id INTEGER,
                tags_ai TEXT,
                tags_legacy TEXT,
                level INTEGER,
                extra_bin TEXT
            )""")
        self.con.commit()

    def create_ticket(self, ticket_id, customer_mail, question, history, thread_id, tags_ai, tags_legacy, level, extra_bin, data, AIResponse, processedcomplaint):
        history_str = ','.join(history)
        tags_ai_str = ','.join(tags_ai)
        tags_legacy_str = ','.join(tags_legacy)

        data = (ticket_id, customer_mail, question, history_str, thread_id, tags_ai_str, tags_legacy_str, level, extra_bin)
        self.cur.execute(
            "INSERT INTO tickets (ticket_id, customer_mail, question, history, thread_id, tags_ai, tags_legacy, level, extra_bin) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            data)
        self.con.commit()

        #res = self.cur.execute("SELECT * FROM tickets")
        #rows = res.fetchall()
        #print(rows)

    def escalate(self):
        pass

    def close(self):
        self.con.close()
        pass

    # deleteticket, getforticket > tags, bin


