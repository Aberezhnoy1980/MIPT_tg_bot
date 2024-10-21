import unittest
from aioresponses import aioresponses

from asset_service.currency_service import get_exchange_rate


class TestCurrencyService(unittest.IsolatedAsyncioTestCase):
    async def test_get_exchange_rate(self):
        currency = 'USD'
        expected_rate = '75.50'

        with aioresponses() as m:
            xml_response = '''
            <ValCurs>
                <Valute>
                    <CharCode>USD</CharCode>
                    <Value>75.50</Value>
                </Valute>
                <Valute>
                    <CharCode>EUR</CharCode>
                    <Value>85.25</Value>
                </Valute>
            </ValCurs>
            '''
            m.get('http://www.cbr.ru/scripts/XML_daily.asp', body=xml_response)

            result = await get_exchange_rate(currency)
            self.assertEqual(result, expected_rate)


if __name__ == '__main__':
    unittest.main()
