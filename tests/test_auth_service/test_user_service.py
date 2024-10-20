import unittest
from datetime import datetime

from faker import Faker

from auth_service.user import User
from auth_service.user_service import is_user_registered, create_user_record, get_user_by_id, get_user_count, \
    get_all_users
from db_handler import SQLiteDB


class TestUserService(unittest.TestCase):
    test_user = User(9999999999999)
    expected_users = set()

    @classmethod
    def setUpClass(cls):
        fake = Faker()
        for _ in range(5):
            tg_id = _
            name = fake.name()
            email = fake.email()
            ts = datetime.now()
            cls.expected_users.add(User(tg_id, name, email))
            with SQLiteDB() as db:
                db.insert_data('users', tg_id, name, email, ts)

    # @unittest.skip("Странный результат")
    def test_is_user_registered(self):
        self.assertFalse(is_user_registered(self.test_user.telegram_id))

    def test_create_user_record(self):
        self.assertFalse(is_user_registered(self.test_user.telegram_id))
        self.assertTrue(create_user_record(self.test_user))
        with SQLiteDB() as db:
            query_result = db.select_data('users', condition=f'telegram_id = {self.test_user.telegram_id}')
        self.assertEqual(len(query_result), 1)
        new_user_from_db_id = query_result[0][0]
        self.assertEqual(new_user_from_db_id, self.test_user.telegram_id)
        self.assertEqual(get_user_by_id(self.test_user.telegram_id), self.test_user)

    def test_get_all_users(self):
        actual_users = {User(t[0], t[1], t[2]) for t in get_all_users()}
        self.assertTrue(self.expected_users.issubset(actual_users))
        self.assertSetEqual(self.expected_users, self.expected_users.intersection(actual_users))

    def test_get_user_count(self):
        with SQLiteDB() as db:
            actual_user_count = db.select_data('users', aggregation='COUNT')[0][0]
        self.assertEqual(get_user_count(), actual_user_count)

    def tearDown(self):
        with SQLiteDB() as db:
            db.delete_data('users', f'telegram_id = {self.test_user.telegram_id}')

    @classmethod
    def tearDownClass(cls):
        with SQLiteDB() as db:
            db.delete_data('users', f'telegram_id = {cls.test_user.telegram_id} or telegram_id between 0 and 4')


if __name__ == '__main__':
    unittest.main()
