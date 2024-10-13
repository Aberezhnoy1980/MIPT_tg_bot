from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.state import StatesGroup, State, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from stock_service.stock import Stock
from stock_service.stock_service import check_stock_existence, get_stock_price_ru, get_stock_price_world, add_stock, \
    get_user_stocks

stock_router = Router()


class CheckStockStates(StatesGroup):
    StockID = State()


class AddStockStates(StatesGroup):
    StockID = State()
    StockPrice = State()
    StockQuantity = State()


@stock_router.message(Command('checkStock'))
async def check_stock_start(message: Message, state: FSMContext):
    await message.reply('Введите идентификатор ценной бумаги')
    await state.set_state(CheckStockStates.StockID)


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
async def check_stock_start(message: Message, state: FSMContext):
    await message.reply('Преступим к добавлению ценной бумаги')
    await message.answer('Введите идентификатор приобретенного инструмента')
    await state.set_state(AddStockStates.StockID)


@stock_router.message(StateFilter(AddStockStates.StockID))
async def add_stock_price(message: Message, state: FSMContext):
    if message.text.lower() != "/stop":
        stock_exists = await check_stock_existence(message.text)
        if stock_exists:
            await message.answer('Введите стоимость единицы ценной бумаги')
            async with state.storage.set_data() as data:
                data['StockID'] = message.text
            print(data)
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
            await state.set_state(AddStockStates.StockQuantity)
        except:
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
            # stock_record = Stock(data['StockOwnerID'], data['StockID'], data['StockPrice'], data['StockQuantity'],
            #                      data['StockPurchaseDate'])
            # add_stock(stock_record)
            print(data)
            await state.clear()
            await message.answer('Информация о приобретенной ценной бумаге успешно сохранена!')
        except:
            await message.reply('Вы некорректно указали количество приобретенных единиц ценной бумаги.')
            await message.answer('Введите количество в виде целого числа или введите /stop для отмены"')

    else:
        await state.clear()
        await message.reply('Добавление информации о приобретенной ценной бумаге отменено')


@stock_router.message(Command('checkPortfolioSummary'))
async def check_portfolio(message: Message):
    user_stocks = get_user_stocks(message.from_user.id)
    portfolio_price = 0
    portfolio_stocks_count = 0
    for stock in user_stocks:
        stock_price = int(stock.quantity) * float(stock.unit_price)
        portfolio_price += stock_price
        portfolio_stocks_count += 1
    await message.reply(f'Вы приобрели {portfolio_stocks_count} раз, на общую сумму {portfolio_price} RUB')
