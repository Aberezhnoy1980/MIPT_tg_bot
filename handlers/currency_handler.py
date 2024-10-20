from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from keyboards.all_kb import currency_services_kb
from utils.asset_states import CheckCurrency
from asset_service.currency_service import get_exchange_rate

currency_router = Router()


@currency_router.callback_query(F.data == "💰Валютный рынок")
async def cmd_stock_services_list(callback: CallbackQuery):
    await callback.message.answer(
        'Можно узнать текущую котировку указанной валюты или посчитать курс на определенную дату',
        reply_markup=currency_services_kb().as_markup())
    await callback.answer()


@currency_router.message(Command('check_exchange'))
async def cmd_exchange_start(message: Message, state: FSMContext):
    await message.reply('Введите идентификатор валюты')
    await state.set_state(CheckCurrency.asset_id_response)


@currency_router.callback_query(F.data == "/check_exchange")
async def check_stock_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите идентификатор валюты')
    await state.set_state(CheckCurrency.asset_id_response)


@currency_router.message(StateFilter(CheckCurrency.asset_id_response))
async def cmd_exchange_rate(message: Message, state: FSMContext):
    currency = message.text.upper()
    exchange_rate = await get_exchange_rate(currency)
    if exchange_rate:
        await message.reply(f'Курс {currency} к рублю сегодня: {exchange_rate} руб.',
                            reply_markup=currency_services_kb().as_markup())
        await state.clear()
    else:
        await message.reply('Извините, не удалось получить информацию о курсе валюты.',
                            reply_markup=currency_services_kb().as_markup())
        await state.clear()
