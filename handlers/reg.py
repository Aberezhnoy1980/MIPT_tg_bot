from aiogram import Router, F
from aiogram.types import CallbackQuery
from auth_service import user_service
from keyboards.all_kb import main_kb
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters.state import StatesGroup, State, StateFilter

from auth_service.user import User

reg_router = Router()


class CheckUserEmail(StatesGroup):
    Email = State()


@reg_router.callback_query(F.data == "registration")
async def cmd_reg(callback: CallbackQuery, state: FSMContext):
    if not user_service.is_user_registered(callback.from_user.id):
        await callback.message.answer('Введите ваш email')
        await state.set_state(CheckUserEmail.Email)
    else:
        await callback.answer(text=f'{callback.from_user.first_name} ты уже зарегистрирован!',
                              show_alert=True)
    await callback.answer()


@reg_router.message(F.text == "/reg")
async def cmd_reg(message: Message, state: FSMContext):
    if not user_service.is_user_registered(message.from_user.id):
        await message.answer('Введите ваш email')
        await state.set_state(CheckUserEmail.Email)
    else:
        await message.answer(text=f'{message.from_user.first_name} ты уже зарегистрирован!')


@reg_router.message(StateFilter(CheckUserEmail.Email))
async def cmd_reg(message: Message, state: FSMContext):
    new_user = User(message.from_user.id, message.from_user.first_name, message.text)
    user_service.create_user_record(new_user)
    await message.answer(f'Регистрация прошла успешно! Привет {message.from_user.first_name}!',
                         reply_markup=main_kb(new_user.telegram_id))
    await state.clear()
