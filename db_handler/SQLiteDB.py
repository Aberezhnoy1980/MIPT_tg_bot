import sqlite3


class SQLiteDB:

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

    def create_table(self, table_name, columns):
        columns_str = ', '.join(columns)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")

    def insert_data(self, table_name, *data):
        placeholders = ', '.join(['?'] * len(data))
        self.cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", data)

    def select_data(self, table_name, columns=None, condition=None):
        if columns:
            columns_str = ', '.join(columns)
        else:
            columns_str = '*'

        if condition:
            self.cursor.execute(f"SELECT {columns_str} FROM {table_name} WHERE {condition}")
        else:
            self.cursor.execute(f"SELECT {columns_str} FROM {table_name}")

        return self.cursor.fetchall()
