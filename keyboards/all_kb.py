from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from create_bot import admins
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="📖 О проекте"),
         KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="📝 Заполнить анкету"),
         KeyboardButton(text="📚 Каталог")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard


def reg_btn():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Пройти регистрацию",
        callback_data="registration")
    )
    return builder


def catalog_kb():
    # В отличие от первой kb воспользуюсь сборщиком
    builder = InlineKeyboardBuilder()
    services = ['📈Фондовый рынок',
                '💰Валютный рынок',
                '🪙Криптовалюты',
                '🌏Новости']
    for s in services:
        builder.add(InlineKeyboardButton(
            text=s,
            callback_data=s
        ))
    builder.adjust(2)
    return builder


def stock_services_kb():
    builder = InlineKeyboardBuilder()
    services = {'Стоимость': '/checkStock',
                'Добавить': '/addStock',
                'ИП': 'checkPortfolioSummary'
                }
    for k, v in services.items():
        builder.add(InlineKeyboardButton(
            text=k,
            callback_data=v
        ))
    builder.adjust(3)
    return builder


def github_btn():
    return (InlineKeyboardBuilder()
            .add(InlineKeyboardButton(text='Присоединиться',
                                      url='https://github.com/Aberezhnoy1980/MIPT_tg_bot/tree/main')))
