import sqlite3
from modules.console import Console


class Ticket_db():
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("modules/functionals/tickets.db")
        self.cur = self.con.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id VARCHAR(255),
                thread_id VARCHAR(255),
                name VARCHAR(255),
                customer_mail VARCHAR(255),
                complaint TEXT,
                history TEXT,
                tags_ai BLOB,
                tags_legacy TEXT,
                level INTEGER,
                extra_bin TEXT
            )""")
        self.con.commit()
        Console.log("connected to db")

    def create_ticket(self, ticket_id, customer_mail, complaint, AIResponse, ai_details, data, ):
        thread_id = data["thread_id"]
        name = data["name"]

        tags_legacy = ""
        history_str = AIResponse
        tags_legacy_str = tags_legacy
        extra_bin = ''
        level = 2

        try:
            sql_data = (ticket_id, thread_id, name, customer_mail, complaint,
                        history_str, ai_details, tags_legacy_str, level, extra_bin)

            self.cur.execute(
                "INSERT INTO tickets (ticket_id, thread_id, name, customer_mail, complaint, history, tags_ai, tags_legacy, level, extra_bin) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                sql_data)
            self.con.commit()
            Console.log("added to db")
        except Exception as e:
            tags_ai_str = "none"
            sql_data = (
                ticket_id, thread_id, name, customer_mail, complaint, history_str, tags_ai_str, tags_legacy_str, level,
                extra_bin)

            self.cur.execute(
                "INSERT INTO tickets (ticket_id, thread_id, name, customer_mail, complaint, history, tags_ai, tags_legacy, level, extra_bin) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                sql_data)
            self.con.commit()
            Console.log("added to db")

    def close(self):
        self.con.close()
        pass

    # deleteticket, getforticket > tags, bin
