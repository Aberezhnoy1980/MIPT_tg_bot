from db_handler import SQLiteDB
import requests
import yfinance
from decouple import config

from stock_service.stock import Stock


def add_stock(stock):
    with SQLiteDB(config('db_name')) as db:
        values = (stock.owner_id, stock.stock_id, stock.quantity, stock.unit_price, stock.purchase_date)
        db.insert_data('stocks', values)


async def check_stock_existence(stock_id):
    url = f'https://iss.moex.com/iss/securities/{stock_id}.json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        exist = data.get('boards', {}).get('data', [])
        return bool(exist) if exist != [] else False
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


def get_user_stocks(owner_id):
    stocks = []
    with SQLiteDB(config('db_name')) as db:
        result = db.select_data('stocks', condition=f'owner_id = {owner_id}')
    for row in result:
        owner_id, stock_id, quantity, unit_price, purchase_date = row
        stock = Stock(owner_id, stock_id, quantity, unit_price, purchase_date)
        stocks.append(stock)
    return stocks
