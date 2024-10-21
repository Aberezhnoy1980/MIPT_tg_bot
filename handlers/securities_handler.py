import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.all_kb import securities_services_kb, portfolio_management_kb
from asset_service.securities_service import check_stock_existence, get_stock_price_ru, get_stock_price_world
from utils.asset_states import CheckStock

logger = logging.getLogger(__name__)
stock_router = Router()


@stock_router.callback_query(F.data == "📈Фондовый рынок")
async def cmd_stock_services_list(callback: CallbackQuery):
    await callback.message.answer(
        'Вы можете узнать текущую рыночную стоимость ценной бумаги, управлять инвестиционным '
        'портфелем, посчитать текущую доходность своего инвестиционного портфеля',
        reply_markup=securities_services_kb().as_markup())
    await callback.answer()


@stock_router.message(Command('check_stock'))
async def check_stock_start(message: Message, state: FSMContext):
    await message.reply('Введите идентификатор ценной бумаги')
    await state.set_state(CheckStock.asset_id_response)


@stock_router.callback_query(F.data == "/check_stock")
async def check_stock_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите идентификатор ценной бумаги')
    await state.set_state(CheckStock.asset_id_response)
    await callback.answer()


@stock_router.message(StateFilter(CheckStock.asset_id_response))
async def check_stock_id(message: Message, state: FSMContext):
    stock_id = message.text.upper()

    stock_existence = check_stock_existence(stock_id)
    if stock_existence:
        stock_price, stock_currency = get_stock_price_ru(stock_id)
        if stock_price is not None:
            await message.reply(
                f"Ценная бумага с идентификатором {stock_id} существует на Московской бирже. "
                f"Текущий курс: {stock_price, stock_currency}", reply_markup=securities_services_kb().as_markup())
        else:
            stock_price = get_stock_price_world(stock_id)
            if stock_price is not None:
                await message.reply(
                    f"Ценная бумага с идентификатором {stock_id} существует на Yahoo! Finance. "
                    f"Текущий курс: {stock_price}", reply_markup=securities_services_kb().as_markup())
            else:
                await message.reply(
                    f"Ценная бумага с идентификатором {stock_id} существует на Московской бирже, но не продается ни в "
                    f"России, ни за рубежом", reply_markup=securities_services_kb().as_markup())
    else:
        await message.reply(
            f"Ценная бумага с идентификатором {stock_id} не найдена ни на Московской бирже, ни на Yahoo! Finance.",
            reply_markup=securities_services_kb().as_markup())
    await state.clear()
