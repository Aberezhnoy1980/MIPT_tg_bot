import unittest

from auth_service.user import User
from auth_service.user_service import is_user_registered, create_user_record
from db_handler import SQLiteDB


class TestUserService(unittest.TestCase):
    test_user = User(9999999999999)

    def tearDown(self):
        with SQLiteDB() as db:
            db.delete_data('users', f'telegram_id = {self.test_user.telegram_id}')

    def test_is_user_registered(self):
        self.assertFalse(is_user_registered(self.test_user.telegram_id))

    def test_create_user_record(self):
        self.assertTrue(create_user_record(self.test_user))
        with SQLiteDB() as db:
            query_result = db.select_data('users', condition=f'telegram_id = {self.test_user.telegram_id}')
        self.assertEqual(len(query_result), 1)
        new_user_from_db = query_result[0][0]
        self.assertEqual(new_user_from_db, self.test_user.telegram_id)


if __name__ == '__main__':
    unittest.main()