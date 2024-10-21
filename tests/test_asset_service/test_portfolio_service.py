import unittest
from unittest.mock import patch, Mock

from asset_service.asset import Asset
from asset_service.portfolio_service import (is_asset_exists_in_db, is_record_exists_in_db,
                                             add_record, delete_record, reset_portfolio, get_user_assets,
                                             calc_portfolio_diff)
from asset_service.securities_service import get_stock_price_ru
from db_handler import SQLiteDB


class TestUserService(unittest.TestCase):
    test_user_id = 9999999999999
    test_asset = Asset('AAPL', 10, 100, test_user_id, '2024-10-21 05:35:20.579702')

    def tearDown(self):
        with SQLiteDB() as db:
            db.delete_data('users', condition=f'telegram_id = {self.test_user_id}')
            db.delete_data('assets', condition=f'asset_id = "{self.test_asset.asset_id}" '
                                               f'and quantity = {self.test_asset.quantity} '
                                               f'and unit_price = {self.test_asset.unit_price}')

    def test_is_asset_exists_in_db(self):
        self.assertFalse(is_asset_exists_in_db(self.test_asset.asset_id))
        self.assertIs(is_asset_exists_in_db(self.test_asset.asset_id), False)

    def test_is_record_exists_in_db(self):
        self.assertFalse(is_record_exists_in_db(self.test_asset.asset_id, self.test_asset.unit_price))

    def test_add_record(self):
        self.assertTrue(add_record(self.test_asset))
        with SQLiteDB() as db:
            asset_from_db = Asset(*db.select_data('assets',
                                                  condition=f'asset_id = "{self.test_asset.asset_id}"')[0])
        self.assertEqual(self.test_asset, asset_from_db)

    def test_delete_record(self):
        self.assertTrue(add_record(self.test_asset))
        self.assertFalse(delete_record(self.test_asset.asset_id, self.test_asset.unit_price))
        with SQLiteDB() as db:
            db_response = db.select_data('assets', condition=f'asset_id = "{self.test_asset.asset_id}"')
        self.assertEqual(db_response, [])

    def test_reset_portfolio(self):
        self.assertTrue(reset_portfolio(self.test_user_id))

    def test_get_user_assets(self):
        self.assertTrue(add_record(self.test_asset))
        db_response = get_user_assets(self.test_user_id)
        self.assertIsNotNone(db_response)
        self.assertIn(self.test_asset, db_response)

    @patch('asset_service.portfolio_service.get_user_assets')
    @patch('asset_service.securities_service.get_stock_price_ru')
    def test_calc_portfolio_diff(self, mock_get_stock_price_ru, mock_get_user_assets):
        # Mocking the return values for the functions
        mock_get_user_assets.return_value = [
            Mock(asset_id='AAPL', quantity='10', unit_price=100.0),
            Mock(asset_id='GOOGL', quantity='5', unit_price=200.0)
        ]
        mock_get_stock_price_ru.side_effect = [(120.0, 'RUB'), (220.0, 'RUB')]

        # Calling the function to test
        result = calc_portfolio_diff(123)

        # Expected values for the test case
        expected_current_price = 10 * 120.0 + 5 * 220.0
        expected_origin_price = 10 * 100.0 + 5 * 200.0

        # Asserting the results
        self.assertEqual(result, (expected_current_price, expected_origin_price))


if __name__ == '__main__':
    unittest.main()
