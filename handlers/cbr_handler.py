from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

currency_router = Router()

# class CheckCurrencyStates:
#
#
# @currency_router.message(Command('checkStock'))
# async def check_stock_start(message: Message, state: FSMContext):
#     await message.reply('Хорошо! Введи тикер ценной бумаги')
#     await state.set_state(CheckCurrencyStates.StockID)
