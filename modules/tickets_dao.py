import sqlite3

class Ticket_db():
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("functionals/tickets.db")
        self.cur = self.con.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id INTEGER,
                customer_mail TEXT,
                question TEXT,
                product_tags TEXT,
                problem_tags TEXT,
                level INTEGER,
                extra_bin TEXT
            )""")
        self.con.commit()

    def add_entry(self, ticket_id, customer_mail, question, product_tags, problem_tags, level, extra_bin):
        product_tags_str = ','.join(product_tags)
        problem_tags_str = ','.join(problem_tags)

        data = (ticket_id, customer_mail, question, product_tags_str, problem_tags_str, level, extra_bin)
        self.cur.execute(
            "INSERT INTO tickets (ticket_id, customer_mail, question, product_tags, problem_tags, level, extra_bin) VALUES (?, ?, ?, ?, ?, ?, ?)",
            data)
        self.con.commit()

        res = self.cur.execute("SELECT * FROM tickets")
        rows= res.fetchall()
        print(rows)

        self.con.close()
