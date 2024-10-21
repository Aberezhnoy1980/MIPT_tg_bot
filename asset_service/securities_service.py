import requests
import yfinance


def check_stock_existence(stock_id: str) -> bool:
    """
    Функция проверяет существование актива по указанным адресам ресурсов.
    :param stock_id: Идентификатор актива
    :return: bool, результат наличия или отсутствия данных в ответе на запрос
    """
    url = f'https://iss.moex.com/iss/securities/{stock_id}.json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('boards', {}).get('data', []) != []
    else:
        return False


def get_stock_price_ru(stock_id: str) -> list:
    """
    Функция запрашивает у сервера MOEX цену актива по указанному адресу поп переданному идентификатору
    :param stock_id: Идентификатор актива
    :return: list, возвращает значение цены и валюты
    """
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


def get_stock_price_world(stock_id: str) -> list:
    """
    Функция запрашивает у сервера Yahoo Finance цену актива по указанному адресу поп переданному идентификатору
    :param stock_id: Идентификатор актива
    :return: list, возвращает значение цены и валюты
    """
    ticker = yfinance.Ticker(stock_id)
    stock_info = ticker.info
    stock_currency = stock_info['currency']
    stock_price = stock_info.get('currentPrice')
    if stock_price is not None:
        return [stock_price, stock_currency]
    else:
        return []
