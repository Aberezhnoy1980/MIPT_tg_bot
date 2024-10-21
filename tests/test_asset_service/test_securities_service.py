import unittest
from unittest import mock

from asset_service.securities_service import check_stock_existence, get_stock_price_ru, get_stock_price_world


class TestSecuritiesService(unittest.TestCase):

    def test_check_stock_existence(self):
        test_stock_id = "AAPL"
        test_url = f"https://iss.moex.com/iss/securities/{test_stock_id}.json"
        test_response_json = {"boards": {"data": [["AAPL"]]}}

        with mock.patch('requests.get') as mock_get:
            mock_response_success = mock.Mock()
            mock_response_success.status_code = 200
            mock_response_success.json.return_value = test_response_json

            mock_response_error = mock.Mock()
            mock_response_error.status_code = 404
            mock_response_error.json.return_value = None

            mock_get.return_value = mock_response_success
            result_success = check_stock_existence(test_stock_id)
            self.assertTrue(result_success)
            mock_get.assert_called_once_with(test_url)

            mock_get.return_value = mock_response_error
            result_error = check_stock_existence(test_stock_id)
            self.assertFalse(result_error)
            mock_get.assert_called_with(test_url)

    def test_get_stock_price_ru(self):
        test_stock_id = "AAPL"
        test_url = f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{test_stock_id}.json?iss.only=securities&securities.columns=PREVPRICE,CURRENCYID"
        test_response_json = {
            "securities": {
                "data": [
                    [100.0, "SUR"]
                ]
            }
        }
        with mock.patch('requests.get') as mock_get:
            mock_response_success = mock.Mock()
            mock_response_success.status_code = 200
            mock_response_success.json.return_value = test_response_json

            mock_response_error = mock.Mock()
            mock_response_error.status_code = 400
            mock_response_error.json.return_value = None

            mock_get.return_value = mock_response_success
            result_success = get_stock_price_ru(test_stock_id)
            self.assertEqual(result_success, [100.0, 'RUB'])

            mock_get.return_value = mock_response_error
            result_error = get_stock_price_ru(test_stock_id)
            self.assertFalse(result_error)

    def test_get_stock_price_world(self):
        test_stock_id = "AAPL"

        with mock.patch('yfinance.Ticker') as mock_ticker:
            mock_ticker_instance = mock_ticker.return_value
            mock_ticker_instance.info = {
                'currency': 'USD',
                'currentPrice': 150.0
            }

            result = get_stock_price_world(test_stock_id)
            self.assertEqual(result, [150.0, 'USD'])
            mock_ticker.assert_called_once_with(test_stock_id)


if __name__ == '__main__':
    unittest.main()
