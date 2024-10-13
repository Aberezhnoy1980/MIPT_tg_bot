from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from auth_service import user_service
from keyboards.all_kb import main_kb

from auth_service.user import User

reg_router = Router()


@reg_router.callback_query(F.data == "registration")
async def cmd_reg(callback: CallbackQuery):
    if not user_service.is_user_registered(callback.from_user.id):
        new_user = User(callback.from_user.id, callback.from_user.first_name)
        user_service.create_user_record(new_user)
        await callback.message.answer(f'Регистрация прошла успешно! Привет {callback.from_user.first_name}!',
                                      reply_markup=main_kb(new_user.telegram_id))
        await callback.answer()
    else:
        await callback.answer(text=f'{callback.from_user.first_name} ты уже зарегистрирован!')
