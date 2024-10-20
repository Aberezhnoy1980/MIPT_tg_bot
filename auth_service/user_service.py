from auth_service.user import User
from db_handler.SQLiteDB import SQLiteDB
from datetime import datetime


def is_user_registered(telegram_id: int) -> bool:
    with SQLiteDB() as db:
        return db.select_data('users', condition=f'telegram_id = {telegram_id}') != []


def create_user_record(user: User) -> bool:
    if not is_user_registered(user.telegram_id):
        with SQLiteDB() as db:
            db.insert_data('users', user.telegram_id, user.name, user.email, datetime.now().strftime("%Y-%m-%d %H:%M"))

    return is_user_registered(user.telegram_id)


def get_all_users():
    with SQLiteDB() as db:
        return db.select_data('users', aggregation='Count')[0][0]
