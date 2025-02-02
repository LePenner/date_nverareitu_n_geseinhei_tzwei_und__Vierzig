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
                tags_legacy BLOB,
                level INTEGER,
                extra_bin TEXT
            )""")
        self.con.commit()

    def create_ticket(self, ticket_id, customer_mail, complaint, AIResponse, ai_details, data, ):
        Console.log("received ticket_id: " + ticket_id)
        Console.log("received customer_mail: " + customer_mail)
        Console.log("received complaint: " + complaint)
        Console.log("received AIResponse:")
        Console.log(AIResponse)
        Console.log("received ai_details:")
        Console.log(ai_details)
        Console.log("received data:")
        Console.log(data)
        Console.log("received all data")
        thread_id = data["thread_id"]
        name = data["name"]

        # no legacy tags?

        tags_legacy = []
        history_str = AIResponse
        tags_legacy_str = tags_legacy
        extra_bin = ''
        level = 2
        Console.log("refactored all data")

        """{'tags': {'product': 'Gardenbeetle', 'problem': ['Will not turn on after submersion in water']}, 'continue': 'employee'}"""
        Console.log("l52")
        try:

            Console.log("l60")
            sql_data = (ticket_id, thread_id, name, customer_mail, complaint,
                        history_str, ai_details, tags_legacy_str, level, extra_bin)
            Console.log("received sql_data:")
            Console.log(sql_data)

            self.cur.execute(
                "INSERT INTO tickets (ticket_id, thread_id, name, customer_mail, complaint, history, tags_ai, tags_legacy, level, extra_bin) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                sql_data)
            self.con.commit()
            Console.log("added to db")
        except Exception as e:
            Console.log("no ai tags recognised:")
            Console.log(e)
            tags_ai_str = "none"
            sql_data = (
                ticket_id, thread_id, name, customer_mail, complaint, history_str, tags_ai_str, tags_legacy_str, level,
                extra_bin)

            self.cur.execute(
                "INSERT INTO tickets (ticket_id, thread_id, name, customer_mail, complaint, history, tags_ai, tags_legacy, level, extra_bin) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                sql_data)
            self.con.commit()
            Console.log("added to db")

        # res = self.cur.execute("SELECT * FROM tickets")
        # rows = res.fetchall()
        # print(rows)

    def escalate(self):
        pass

    def close(self):
        self.con.close()
        pass

    # deleteticket, getforticket > tags, bin
