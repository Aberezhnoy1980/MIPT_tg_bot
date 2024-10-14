from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from auth_service import user_service
from keyboards.all_kb import main_kb, reg_btn, catalog_kb

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    if user_service.is_user_registered(user_id):
        await message.answer(f'Привет {message.from_user.first_name}!', reply_markup=main_kb(message.from_user.id))
    else:
        await message.answer('Привет! Я дружелюбный бот и могу помогать в финансовых вопросах. Мы еще не знакомы, '
                             'поэтому прошу тебя зарегистрироваться', reply_markup=reg_btn().as_markup())


@start_router.message(F.text == '/start_3')
async def cmd_start_3(message: Message):
    await message.answer('Запуск сообщения по команде /start_3 используя магический фильтр F.text!')


@start_router.message(F.text == '📚 Каталог')
async def cmd_catalog(message: Message):
    await message.answer('Выберите категорию', reply_markup=catalog_kb().as_markup())
