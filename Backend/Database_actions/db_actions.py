import psycopg2
from psycopg2 import Error

class DatabseActions:
    def __init__(self):
        self.connection = psycopg2.connect(
            user="janjohannsen",
            password="flensburg",
            host="localhost",
            database="test_db",
        )
        self.cursor = self.connection.cursor()

    def fetch_columns_from_table(self):
        self.cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'transactions'")
        columns = self.cursor.fetchall()
        return columns

    def insert_into_table(self, name, amount, category):
        self.cursor.execute("INSERT INTO transactions (name, amount, category) VALUES (%s, %s, %s)", (name, amount, category))
        self.connection.commit()

    def get_transaction_by_id(self, id):
        self.cursor.execute("SELECT * FROM transactions WHERE id = %s", (id,))
        entry = self.cursor.fetchone()
        if entry:
            return {"id": entry[0], "name": entry[1], "amount": entry[2], "category": entry[3]}
        return None

    def delete_from_table(self, name, amount, category):
        self.cursor.execute("DELETE FROM transactions WHERE name = %s AND amount = %s AND category = %s", (name, amount, category))
        self.connection.commit()

    def update_from_table(self, name, amount, category):
        self.cursor.execute("UPDATE transactions SET amount = %s WHERE name = %s AND category = %s", (amount, name, category))
        self.connection.commit()

    def delete_all_entries(self):
        self.cursor.execute("DELETE FROM transactions")
        self.connection.commit()

    def show_all_entries(self):
        self.cursor.execute("SELECT * FROM transactions")
        entries = self.cursor.fetchall()
        return [{"id": entry[0], "name": entry[1], "amount": entry[2], "category": entry[3]} for entry in entries]

    def delete_from_id(self, id):
        self.cursor.execute("DELETE FROM transactions WHERE id = %s", (id,))
        self.connection.commit()
