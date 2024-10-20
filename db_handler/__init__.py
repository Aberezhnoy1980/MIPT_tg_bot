import os
from db_handler.SQLiteDB import SQLiteDB
from create_bot import root_path

db_path = os.path.join(root_path, 'app_data')
if not os.path.exists(db_path):
    os.mkdir(db_path)

with SQLiteDB() as db:
    user_columns = ['telegram_id INTEGER PRIMARY KEY',
                    'name TEXT',
                    'email TEXT',
                    'registration_timestamp DATA']
    db.create_table('users', user_columns)
    stock_columns = ['asset_id TEXT',
                     'quantity INTEGER',
                     'unit_price REAL',
                     'owner_id INTEGER',
                     'asset_type TEXT',
                     'purchase_date TIMESTAMP',
                     'PRIMARY KEY (asset_id, unit_price, owner_id)',
                     'FOREIGN KEY (owner_id) REFERENCES users(telegram_id) ON DELETE CASCADE']
    db.create_table('assets', stock_columns)
