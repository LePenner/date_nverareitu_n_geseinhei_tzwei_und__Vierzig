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
                tags_ai TEXT,
                tags_legacy TEXT,
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
        tags_legacy = []
        history_str = AIResponse
        tags_legacy_str = ','.join(tags_legacy)
        extra_bin = ''
        level = 2
        Console.log("refactored all data")

        """ai_details = {
            "Problems": [
                {
                    "description": "Battery explosion",
                    "tags": ["physical problem", "battery issue"],
                    "Continue": "employe"
                }
            ]
        }"""
        Console.log("l52")
        try:
            problems = ai_details["Problems"]
            Console.log("l54")
            for problem in problems:
                Console.log("l56")
                tags_ai = problem["tags"]
                Console.log("l58")
                tags_ai_str = ','.join(tags_ai)
                Console.log("l60")
                sql_data = (ticket_id, thread_id, name, customer_mail, complaint, history_str, tags_ai_str, tags_legacy_str, level, extra_bin)
                Console.log("received sql_data:")
                Console.log(sql_data)

                self.cur.execute(
                    "INSERT INTO tickets (ticket_id, thread_id, name, customer_mail, complaint, history, tags_ai, tags_legacy, level, extra_bin) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    sql_data)
                self.con.commit()
                Console.log("added to db")
        except Exception as e:
            Console.log("no ai tags recognised: " + e)
            tags_ai_str = "none"
            sql_data = (
            ticket_id, thread_id, name, customer_mail, complaint, history_str, tags_ai_str, tags_legacy_str, level,
            extra_bin)

            self.cur.execute(
                "INSERT INTO tickets (ticket_id, thread_id, name, customer_mail, complaint, history, tags_ai, tags_legacy, level, extra_bin) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                sql_data)
            self.con.commit()
            Console.log("added to db")



        #res = self.cur.execute("SELECT * FROM tickets")
        #rows = res.fetchall()
        #print(rows)

    def escalate(self):
        pass

    def close(self):
        self.con.close()
        pass

    # deleteticket, getforticket > tags, bin


