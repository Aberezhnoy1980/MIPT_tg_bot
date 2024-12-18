from typing import Union

from asset_service.currency_service import get_exchange_rate
from db_handler import SQLiteDB
from asset_service.asset import Asset
from asset_service.securities_service import get_stock_price_ru


def is_asset_exists_in_db(asset_id: str) -> bool:
    """
    Функция проверяет наличие записи в базе данных актива по переданному идентификатору.
    :param asset_id:
    :return: Boolean
    """
    condition = f'asset_id = "{asset_id}"'
    with SQLiteDB() as db:
        result = db.select_data('assets', condition=condition)
    return result != []


def is_record_exists_in_db(asset_id: str, unit_price: float) -> bool:
    """
    Функция проверяет наличие записи в базе данных.
    :param asset_id:
    :param unit_price:
    :return:Boolean
    """
    condition = f'asset_id = "{asset_id}" and unit_price = {unit_price}'
    with SQLiteDB() as db:
        result = db.select_data('assets', condition=condition)
    return result != []


def add_record(asset: Asset) -> bool:
    """
    Функция для добавления записи об активе в базу данных.
    :param asset: Экземпляр класс Asset
    :return: Boolean, результат вызова функции is_record_existence.
    """
    with SQLiteDB() as db:
        values = (asset.asset_id,
                  asset.quantity,
                  asset.unit_price,
                  asset.owner_id,
                  asset.purchase_date)
        db.insert_data('assets', *values)
    return is_record_exists_in_db(asset.asset_id, asset.unit_price)


def delete_record(asset_id: str, unit_price: float) -> bool:
    """
      Сброс всех записей в таблице базы данных
      :param asset_id: id пользователя для условия выборки из БД
      :param unit_price: номинальная цена актива
      :return: Boolean, результат проверки наличия записей в таблице БД по фильтру переданного owner_id
      """
    condition: str = f'asset_id = "{asset_id}" and unit_price = {unit_price}'
    with SQLiteDB() as db:
        db.delete_data('assets', condition=condition)
    return is_record_exists_in_db(asset_id, unit_price)


def reset_portfolio(user_id: int) -> bool:
    """
      Сброс всех записей в таблице базы данных
      :param user_id: id пользователя для условия выборки из БД
      :return: Boolean
      """
    condition: str = f'owner_id = {user_id}'
    with SQLiteDB() as db:
        db.delete_data('assets', condition=condition)
    with SQLiteDB() as db:
        return db.select_data('assets', condition=f'owner_id = {user_id}') == []


def get_user_assets(user_id: int) -> list:
    """
    Функция возвращает список записей из базы данных.
    :param user_id:
    :return: List активов пользователя
    """
    assets = []
    with SQLiteDB() as db:
        result = db.select_data('assets', condition=f'owner_id = {user_id}')
    for row in result:
        asset_id, quantity, unit_price, user_id, purchase_date = row
        asset = Asset(asset_id, quantity, unit_price, user_id, purchase_date)
        assets.append(asset)
    return assets


async def calc_portfolio_diff(user_id: int) -> Union[tuple[float, float], None]:
    """
    Функция для анализа отклонения текущей стоимости портфеля от номинальной.
    :param user_id:
    :return: Tuple, содержащий текущую номинальную стоимость активов
    """
    user_stocks = get_user_assets(user_id)
    if not user_stocks:
        return None
    origin_portfolio_price = 0
    current_portfolio_price = 0
    for stock in user_stocks:
        if get_stock_price_ru(stock.asset_id):
            current_price = get_stock_price_ru(stock.asset_id)[0]
            current_stock_price = int(stock.quantity) * float(current_price)
            current_portfolio_price += current_stock_price
        elif await get_exchange_rate(stock.asset_id):
            current_price = await get_exchange_rate(stock.asset_id)
            current_stock_price = int(stock.quantity) * float(current_price.replace(',', '.'))
            current_portfolio_price += current_stock_price
        origin_stock_price = int(stock.quantity) * float(stock.unit_price)
        origin_portfolio_price += origin_stock_price
    return current_portfolio_price, origin_portfolio_price
