import sqlite3
import os
from create_bot import root_path


class SQLiteDB:

    def __init__(self, db_name=None):
        self.db_name = os.path.join(root_path, 'app_data/database.db') if db_name is None else db_name

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

    def delete_data(self, table_name, condition=None):
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")

    def select_data(self, table_name, aggregation=None, columns=None, condition=None):
        if columns:
            columns_str = ', '.join(columns)
        else:
            columns_str = '*'

        if aggregation:
            select_expr_str = f'{aggregation}({columns_str})'
        else:
            select_expr_str = columns_str

        if condition:
            self.cursor.execute(f"SELECT {select_expr_str} FROM {table_name} WHERE {condition}")
        else:
            self.cursor.execute(f"SELECT {select_expr_str} FROM {table_name}")

        return self.cursor.fetchall()
