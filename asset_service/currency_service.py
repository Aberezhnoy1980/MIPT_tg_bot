import aiohttp
from decouple import config
from xml.etree import ElementTree


async def get_exchange_rate(currency):
    url = config('CBR_URL')
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            xml_string = await response.text()
            root = ElementTree.fromstring(xml_string)
            currency_rate = None
            for valute in root.findall('.//Valute'):
                if valute.find('./CharCode').text == currency:
                    currency_rate = valute.find('./Value').text
                    break
            return currency_rate
