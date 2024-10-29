from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from asset_service.currency_service import get_exchange_rate
from keyboards.all_kb import portfolio_management_kb
from asset_service.asset import Asset
from asset_service.securities_service import check_stock_existence
from asset_service.portfolio_service import add_record, calc_portfolio_diff, is_record_exists_in_db, \
    is_asset_exists_in_db, delete_record, reset_portfolio
from utils.asset_states import AddAsset, DeleteAsset
from create_bot import logger

portfolio_router = Router()


@portfolio_router.callback_query(F.data == "/asset_management")
async def cmd_portfolio_services_list(callback: CallbackQuery):
    await callback.message.answer(
        'Вы можете добавлять, удалять ценные бумаги и другие активы, '
        'а также анализировать свой инвестиционный портфель',
        reply_markup=portfolio_management_kb().as_markup())
    await callback.answer()


@portfolio_router.message(Command('add_asset'))
async def add_stock_start(message: Message, state: FSMContext):
    await message.reply('Преступим к добавлению ценной бумаги')
    await message.answer('Введите идентификатор приобретенного инструмента')
    await state.set_state(AddAsset.asset_id_response)


@portfolio_router.callback_query(F.data == "/add_asset")
async def add_stock_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите идентификатор приобретенного актива')
    await state.set_state(AddAsset.asset_id_response)
    await callback.answer()


@portfolio_router.message(StateFilter(AddAsset.asset_id_response))
async def add_stock_price(message: Message, state: FSMContext):
    if message.text.lower() != "/stop":
        asset = message.text
        # TODO currency_exist = await get_exchange_rate(asset)
        if check_stock_existence(asset) or get_exchange_rate(asset):
            await state.update_data(asset_id=message.text.upper())
            await message.answer('Введите стоимость единицы актива')
            await state.set_state(AddAsset.unit_price_response)
        else:
            await message.reply(
                'Указанный идентификатор актива не найден на Московской бирже, Yahoo! Finance или Центральном банке.')
            await message.answer('Введите корректный идентификатор приобретенного инструмента или введите /stop для '
                                 'отмены')
    else:
        await message.reply('Добавление информации о приобретенном активе отменено',
                            reply_markup=portfolio_management_kb().as_markup())
        await state.clear()


@portfolio_router.message(StateFilter(AddAsset.unit_price_response))
async def add_stock_quantity(message: Message, state: FSMContext):
    if message.text.lower() != '/stop':
        try:
            await state.update_data(unit_price=float(message.text.replace(',', '.')))
            await message.answer('Введите количество приобретенных единиц инструмента')
            await state.set_state(AddAsset.quantity_response)
        except Exception as e:
            logger.info(e)
            await message.reply('Вы некорректно указали стоимость актива.')
            await message.answer('Введите стоимость приобретения в числовом формате или введите /stop для отмены"')
    else:
        await message.reply('Добавление информации о приобретенном активе отменено',
                            reply_markup=portfolio_management_kb().as_markup())
        await state.clear()


@portfolio_router.message(StateFilter(AddAsset.quantity_response))
async def add_stock_finish(message: Message, state: FSMContext):
    if message.text.lower() != "/stop":
        try:
            await state.update_data(quantity=int(message.text))
            data = await state.get_data()
            new_asset = Asset(data['asset_id'],
                              data['quantity'],
                              data['unit_price'],
                              message.from_user.id,
                              datetime.now())
            try:
                add_record(new_asset)
            except Exception as e:
                logger.info(e)
            await message.answer('Информация о приобретенном активе успешно сохранена!',
                                 reply_markup=portfolio_management_kb().as_markup())
            await state.clear()
        except Exception as e:
            logger.info(e)
            await message.reply('Вы некорректно указали количество.')
            await message.answer('Введите количество в виде целого числа или введите /stop для отмены')
    else:
        await message.reply('Добавление информации о приобретенном активе отменено',
                            reply_markup=portfolio_management_kb().as_markup())
        await state.clear()


@portfolio_router.message(Command('delete_asset'))
async def delete_stock_start(message: Message, state: FSMContext):
    await message.answer('Для удаления позиции ведите идентификатор актива')
    await state.set_state(DeleteAsset.asset_id_response)


@portfolio_router.callback_query(F.data == "/delete_asset")
async def delete_stock_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Для удаления позиции ведите идентификатор актива')
    await state.set_state(DeleteAsset.asset_id_response)
    await callback.answer()


@portfolio_router.message(StateFilter(DeleteAsset.asset_id_response))
async def delete_asset(message: Message, state: FSMContext):
    if message.text.lower() != "/stop":
        asset_id = message.text.upper()
        if is_asset_exists_in_db(asset_id):
            await state.update_data(asset_id=asset_id)
            await message.answer('Введите номинальную стоимость для актива')
            await state.set_state(DeleteAsset.unit_price_response)
        else:
            await message.reply(f'В вашем инвестиционном портфеле актива {asset_id} не найдено.')
            await message.answer('Введите корректный идентификатор актива и его номинальную стоимость или введите '
                                 '/stop для отмены')
    else:
        await message.reply('Удаление информации о приобретенной ценной бумаге отменено',
                            reply_markup=portfolio_management_kb().as_markup())
        await state.clear()


@portfolio_router.message(StateFilter(DeleteAsset.unit_price_response))
async def delete_asset(message: Message, state: FSMContext):
    if message.text.lower() != "/stop":
        unit_price = float(message.text.replace(',', '.'))
        data = await state.get_data()
        asset_id = data['asset_id']
        if is_record_exists_in_db(asset_id, unit_price):
            await state.update_data(asset_id=message.text.upper())
            try:
                delete_record(asset_id, unit_price)
            except Exception as e:
                logger.info(e)
            await message.answer('Информация о приобретенной ценной бумаге успешно удалена!',
                                 reply_markup=portfolio_management_kb().as_markup())
            await state.clear()
        else:
            await message.reply(f'В вашем инвестиционном портфеле актива {asset_id} с номинальной  стоимостью '
                                f'{unit_price} не найдено.')
            await message.answer('Введите корректный идентификатор актива и его номинальную стоимость или введите '
                                 '/stop для отмены')
    else:
        await message.reply('Удаление информации о приобретенной ценной бумаге отменено',
                            reply_markup=portfolio_management_kb().as_markup())
        await state.clear()


@portfolio_router.message(Command('reset_portfolio'))
async def delete_stock_start(message: Message, state: FSMContext):
    await message.answer('Вы уверены что хотите удалить свой инвестиционный портфель?')
    await state.set_state(DeleteAsset.asset_id_response)


@portfolio_router.callback_query(F.data == "/reset_portfolio")
async def delete_stock_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Вы уверены что хотите удалить свой инвестиционный портфель?')
    await state.set_state(DeleteAsset.choice_response)
    await callback.answer()


@portfolio_router.message(StateFilter(DeleteAsset.choice_response))
async def delete_asset(message: Message, state: FSMContext):
    if message.text == 'да'.lower():
        try:
            reset_portfolio(message.from_user.id)
        except Exception as e:
            logger.info(e)
        await message.answer('Все данные по вашим активам успешно удалены!',
                             reply_markup=portfolio_management_kb().as_markup())
        await state.clear()
    elif message.text == 'нет'.lower():
        await message.reply('Удаление инвестиционного портфеля отменено',
                            reply_markup=portfolio_management_kb().as_markup())
    else:
        await message.answer('Необходимо подтвердить да или нет')
        await state.clear()


@portfolio_router.callback_query(F.data == "/portfolio_summary")
async def check_portfolio(callback: CallbackQuery):
    if await calc_portfolio_diff(callback.from_user.id) is None:
        await callback.message.answer(f'Вы еще не сформировали свой инвестиционный портфель.',
                                      reply_markup=portfolio_management_kb().as_markup())
    else:
        current_portfolio_price, origin_portfolio_price = await calc_portfolio_diff(callback.from_user.id)
        if current_portfolio_price < origin_portfolio_price:
            absolute_profitability = f'Прибыль: 📉<b>{(current_portfolio_price - origin_portfolio_price):,.2f}</b>'
            relative_profitability = f'или <b>{(current_portfolio_price / origin_portfolio_price - 1) * 100:,.2f} %</b>' \
                if origin_portfolio_price != 0 \
                else ''
        else:
            absolute_profitability = f'Прибыль: 📈<b>{(current_portfolio_price - origin_portfolio_price):,.2f}</b>'
            relative_profitability = f'или <b>{(current_portfolio_price / origin_portfolio_price - 1) * 100:,.2f} %</b>' \
                if origin_portfolio_price != 0 \
                else ''
        await callback.message.answer(f'Инвестиционный портфель:\n'
                                      f'Номинальная стоимость: <b>{origin_portfolio_price:,.2f} RUB</b>\n'
                                      f'Текущая стоимость: <b>{current_portfolio_price:,.2f} RUB</b>\n'
                                      f'{absolute_profitability} '
                                      f'{relative_profitability}', reply_markup=portfolio_management_kb().as_markup())
        await callback.answer()


@portfolio_router.message(F.text == '/portfolio_summary')
async def check_portfolio(message: Message):
    if await calc_portfolio_diff(message.from_user.id) is None:
        await message.answer(
            f'Вы еще не сформировали свой инвестиционный портфель.', reply_markup=portfolio_management_kb().as_markup())
    else:
        current_portfolio_price, origin_portfolio_price = calc_portfolio_diff(message.from_user.id)
        if current_portfolio_price < origin_portfolio_price:
            absolute_profitability = f'Прибыль: 📉<b>{(current_portfolio_price - origin_portfolio_price):,.2f}</b>'
            relative_profitability = f'или <b>{(current_portfolio_price / origin_portfolio_price - 1) * 100:,.2f} %</b>' \
                if origin_portfolio_price != 0 \
                else ''
        else:
            absolute_profitability = f'Прибыль: 📈<b>{(current_portfolio_price - origin_portfolio_price):,.2f}</b>'
            relative_profitability = f'или <b>{(current_portfolio_price / origin_portfolio_price - 1) * 100:,.2f} %</b>' \
                if origin_portfolio_price != 0 \
                else ''
        await message.answer(f'Инвестиционный портфель:\n'
                             f'Номинальная стоимость: <b>{origin_portfolio_price:,.2f} RUB</b>\n'
                             f'Текущая стоимость: <b>{current_portfolio_price:,.2f} RUB</b>\n'
                             f'{absolute_profitability} '
                             f'{relative_profitability}', reply_markup=portfolio_management_kb().as_markup())
