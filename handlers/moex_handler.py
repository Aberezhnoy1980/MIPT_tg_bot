from datetime import datetime
import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.filters.state import StatesGroup, State, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.all_kb import stock_services_kb
from stock_service.stock import Stock
from stock_service.stock_service import check_stock_existence, get_stock_price_ru, get_stock_price_world, add_stock, \
    calc_portfolio_diff

logger = logging.getLogger(__name__)
stock_router = Router()


class CheckStockStates(StatesGroup):
    StockID = State()


class AddStockStates(StatesGroup):
    StockID = State()
    StockPrice = State()
    StockQuantity = State()


@stock_router.callback_query(F.data == "📈Фондовый рынок")
async def cmd_stock_services_list(callback: CallbackQuery):
    await callback.message.answer(
        'Выберите операцию с ценными бумагами MOEX: узнать текщую рыночную стоимость, добавить бумагу в портфель, '
        'посчитать текущую доходность своего инвестиционного портфеля',
        reply_markup=stock_services_kb().as_markup())
    await callback.answer()


@stock_router.message(Command('checkStock'))
async def check_stock_start(message: Message, state: FSMContext):
    await message.reply('Введите идентификатор ценной бумаги')
    await state.set_state(CheckStockStates.StockID)


@stock_router.callback_query(F.data == "/checkStock")
async def check_stock_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите идентификатор ценной бумаги')
    await state.set_state(CheckStockStates.StockID)
    await callback.answer()


@stock_router.message(StateFilter(CheckStockStates.StockID))
async def check_stock_id(message: Message, state: FSMContext):
    stock_id = message.text.upper()

    stock_existence = await check_stock_existence(stock_id)
    if stock_existence:
        stock_price, stock_currency = await get_stock_price_ru(stock_id)
        if stock_price is not None:
            await message.reply(
                f"Ценная бумага с идентификатором {stock_id} существует на Московской бирже. Текущий курс: {stock_price}")
        else:
            stock_price = await get_stock_price_world(stock_id)
            if stock_price is not None:
                await message.reply(
                    f"Ценная бумага с идентификатором {stock_id} существует на Yahoo! Finance. Текущий курс: {stock_price}")
            else:
                await message.reply(
                    f"Ценная бумага с идентификатором {stock_id} существует на Московской бирже, но не продается ни в "
                    f"России, ни за рубежом")
    else:
        await message.reply(
            f"Ценная бумага с идентификатором {stock_id} не найдена ни на Московской бирже, ни на Yahoo! Finance.")

    await state.clear()


@stock_router.message(Command('addStock'))
async def add_stock_start(message: Message, state: FSMContext):
    await message.reply('Преступим к добавлению ценной бумаги')
    await message.answer('Введите идентификатор приобретенного инструмента')
    await state.set_state(AddStockStates.StockID)


@stock_router.callback_query(F.data == "/addStock")
async def add_stock_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите идентификатор приобретенного инструмента')
    await state.set_state(AddStockStates.StockID)
    await callback.answer()


@stock_router.message(StateFilter(AddStockStates.StockID))
async def add_stock_price(message: Message, state: FSMContext):
    if message.text.lower() != "/stop":
        stock_exists = await check_stock_existence(message.text)
        if stock_exists:
            await message.answer('Введите стоимость единицы ценной бумаги')
            data = await state.get_data()
            data['StockID'] = message.text
            await state.set_data(data)
            await state.set_state(AddStockStates.StockPrice)
        else:
            await message.reply(
                'Указанный идентификатор ценной бумаги не найден ни на Московской бирже, ни на Yahoo! Finance.')
            await message.answer('Введите корректный идентификатор приобретенного инструмента или введите /stop для '
                                 'отмены')
    else:
        await state.clear()
        await message.reply('Добавление информации о приобретенной ценной бумаге отменено')


@stock_router.message(StateFilter(AddStockStates.StockPrice))
async def add_stock_quantity(message: Message, state: FSMContext):
    if message.text.lower() != '/stop':
        try:
            float(message.text.replace(',', '.'))
            await message.answer('Введите количество приобретенных единиц инструмента')
            data = await state.get_data()
            data['StockPrice'] = message.text.replace(',', '.')
            await state.set_data(data)
            await state.set_state(AddStockStates.StockQuantity)
        except Exception as e:
            logger.info(e)
            await message.reply('Вы некорректно указали стоимость одной ценной бумаги.')
            await message.answer('Введите стоимость приобретения в числовом формате или введите /stop для отмены"')
    else:
        await state.clear()
        await message.reply('Добавление информации о приобретенной ценной бумаге отменено')


@stock_router.message(StateFilter(AddStockStates.StockQuantity))
async def add_stock_finish(message: Message, state: FSMContext):
    if message.text.lower() != "/stop":
        try:
            int(message.text)
            data = await state.get_data()
            data['StockQuantity'] = message.text
            data['StockOwnerID'] = message.from_user.id
            data['StockPurchaseDate'] = datetime.now()
            stock_record = Stock(data['StockOwnerID'],
                                 data['StockID'],
                                 data['StockQuantity'],
                                 data['StockPrice'],
                                 data['StockPurchaseDate'])
            try:
                add_stock(stock_record)
            except Exception as e:
                print(f"Ошибка при добавлении записи в базу данных: {e}")
                await message.answer('База не пишет')
            await state.clear()
            await message.answer('Информация о приобретенной ценной бумаге успешно сохранена!')
        except Exception as e:
            logger.info(e)
            await message.reply('Вы некорректно указали количество приобретенных единиц ценной бумаги.')
            await message.answer('Введите количество в виде целого числа или введите /stop для отмены"')
    else:
        await state.clear()
        await message.reply('Добавление информации о приобретенной ценной бумаге отменено')


@stock_router.callback_query(F.data == "checkPortfolioSummary")
async def check_portfolio(callback: CallbackQuery):
    current_portfolio_price, origin_portfolio_price = await calc_portfolio_diff(callback.from_user.id)
    if current_portfolio_price < origin_portfolio_price:
        absolute_profitability = f'Прибыль: 📉<b>{(current_portfolio_price - origin_portfolio_price):,.2f}</b>'
        relative_profitability = f'или <b>{(current_portfolio_price / origin_portfolio_price - 1) * 100:,.2f}</b>'
    else:
        absolute_profitability = f'Прибыль: 📈<b>{(current_portfolio_price - origin_portfolio_price):,.2f}</b>'
        relative_profitability = f'или <b>{(current_portfolio_price / origin_portfolio_price - 1) * 100:,.2f}</b>'
    await callback.message.answer(f'Инвестиционный портфель:\n'
                                  f'Номинальная стоимость: <b>{origin_portfolio_price:,.2f} RUB</b>\n'
                                  f'Текущая стоимость: <b>{current_portfolio_price:,.2f} RUB</b>\n'
                                  f'{absolute_profitability} '
                                  f'{relative_profitability} %')
    await callback.answer()


@stock_router.message(F.text == '/checkPortfolioSummary')
async def check_portfolio(message: Message):
    current_portfolio_price, origin_portfolio_price = await calc_portfolio_diff(message.from_user.id)
    if current_portfolio_price < origin_portfolio_price:
        absolute_profitability = f'Прибыль: 📉<b>{(current_portfolio_price - origin_portfolio_price):,.2f}</b>'
        relative_profitability = f'или <b>{(current_portfolio_price / origin_portfolio_price - 1):,.2f}</b>'
    else:
        absolute_profitability = f'Прибыль: 📈<b>{(current_portfolio_price - origin_portfolio_price):,.2f}</b>'
        relative_profitability = f'или <b>{(current_portfolio_price / origin_portfolio_price - 1):,.2f}</b>'
    await message.answer(f'Инвестиционный портфель:\n'
                         f'Номинальная стоимость: <b>{origin_portfolio_price:,.2f} RUB</b>\n'
                         f'Текущая стоимость: <b>{current_portfolio_price:,.2f} RUB</b>\n'
                         f'{absolute_profitability} '
                         f'{relative_profitability} %')
