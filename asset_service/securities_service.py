import requests
import yfinance


async def check_stock_existence(stock_id):
    url = f'https://iss.moex.com/iss/securities/{stock_id}.json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        exist = data.get('boards', {}).get('data', [])
        # return bool(exist) if exist != [] else False
        return exist != []
    else:
        return False


async def get_stock_price_ru(stock_id):
    url = f'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{stock_id}.json?iss.only=securities&securities.columns=PREVPRICE,CURRENCYID'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        data = data.get('securities').get('data')
        stock_price = data[0][0]
        stock_currency = data[0][1]
        if stock_currency == 'SUR':
            stock_currency = 'RUB'
    else:
        return []
    return [stock_price, stock_currency]


async def get_stock_price_world(stock_id):
    ticker = yfinance.Ticker(stock_id)
    stock_info = ticker.info
    stock_currency = stock_info['currency']
    stock_price = stock_info.get('currentPrice')
    if stock_price is not None:
        return [stock_price, stock_currency]
    else:
        return []
