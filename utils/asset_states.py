from aiogram.filters.state import StatesGroup, State


class CheckStock(StatesGroup):
    asset_id_response = State()
    unit_price_response = State()
    quantity_response = State()


class AddAsset(StatesGroup):
    asset_id_response = State()
    unit_price_response = State()
    quantity_response = State()


class DeleteAsset(StatesGroup):
    asset_id_response = State()
    unit_price_response = State()
    choice_response = State()


class CheckCurrency(StatesGroup):
    asset_id_response = State()
