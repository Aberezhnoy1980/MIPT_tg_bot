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


def get_user_by_id(telegram_id: int) -> User:
    with SQLiteDB() as db:
        telegram_id, name, email, ts = db.select_data('users', condition=f'telegram_id = {telegram_id}')[0]
        return User(telegram_id, name, email)


def get_user_count():
    with SQLiteDB() as db:
        return db.select_data('users', aggregation='Count')[0][0]


def get_all_users():
    with SQLiteDB() as db:
        return db.select_data('users')
