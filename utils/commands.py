from aiogram.types import BotCommand, BotCommandScopeDefault
from create_bot import bot, admins
from auth_service.user_service import get_all_users


async def set_commands():
    """
    Создание списка команд
    :return: установка списка команд
    """
    commands = [
        BotCommand(command='start', description='Начало работы'),
        BotCommand(command='reg', description='Регистрация пользователя'),
        BotCommand(command='about', description='Информация о проекте'),
        BotCommand(command='add_asset', description='Добавление актива в портфель'),
        BotCommand(command='delete_asset', description='Удавление актива из портфеля'),
        BotCommand(command='reset_portfolio', description='Сброс портфеля'),
        BotCommand(command='check_stock', description='Получение текущей котировки акции'),
        BotCommand(command='check_exchange', description='Получение текущей котировки валюты')
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    """
    Функция, которая выполнится когда бот начнет свою работу.
    :return: Выводит сообщение администраторам бота
    """
    await set_commands()
    count_users = await get_all_users()
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, f'Я запущен🥳. Сейчас в базе данных <b>{count_users}</b> пользователей.')
    except:
        pass


async def stop_bot():
    """
    Функция, которая выполнится когда бот завершит свою работу.
    :return: Выводит сообщение администраторам бота.
    """
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, 'Бот остановлен. За что?😔')
    except:
        pass
