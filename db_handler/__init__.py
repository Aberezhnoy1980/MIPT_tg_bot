import os

from db_handler.SQLiteDB import SQLiteDB

if not os.path.exists('app_data'):
    os.mkdir('app_data')

with SQLiteDB('app_data/my_database.db') as db:
    user_columns = ['telegram_id INTEGER PRIMARY KEY', 'name TEXT', 'email TEXT', 'registration_timestamp DATA']
    db.create_table('users', user_columns)
    stock_columns = ['stock_id TEXT',
                     'quantity INTEGER',
                     'unit_price REAL',
                     'owner_id INTEGER',
                     'purchase_date TIMESTAMP',
                     'FOREIGN KEY (owner_id) REFERENCES users(telegram_id) ON DELETE CASCADE']
    db.create_table('stocks', stock_columns)
