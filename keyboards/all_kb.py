from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from create_bot import admins
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="📖 О нас"), KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="📝 Заполнить анкету"), KeyboardButton(text="📚 Каталог")]
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


def reg_button():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Пройти регистрацию",
        callback_data="registration")
    )
    return builder
