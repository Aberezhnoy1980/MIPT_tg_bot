from db_handler.SQLiteDB import SQLiteDB
from datetime import datetime
from decouple import config


def is_user_registered(telegram_id):
    with (SQLiteDB(config('db_name')) as db):
        return False if db.select_data('users', condition=f'telegram_id = {telegram_id}') == [] else True


def create_user_record(user) -> bool:
    if not is_user_registered(user.telegram_id):
        with SQLiteDB(config('db_name')) as db:
            db.insert_data('users', user.telegram_id, user.name, user.email, datetime.now().strftime("%Y-%m-%d %H:%M"))

    return is_user_registered(user.telegram_id)
