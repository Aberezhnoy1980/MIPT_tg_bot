import requests
import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State, StateFilter

from keyboards.all_kb import main_kb
from ygpt_service.ygpt_service import get_iam_token, send_request

ygpt_router = Router()

logger = logging.getLogger(__name__)


class CheckUserQuestion(StatesGroup):
    user_question = State()


@ygpt_router.message(F.text == '❓ Спросить GPT')
async def process_message(message: Message, state: FSMContext):
    await message.answer('Задавай любой вопрос!')
    await state.set_state(CheckUserQuestion.user_question)


@ygpt_router.message(StateFilter(CheckUserQuestion.user_question))
async def process_message(message: Message, state: FSMContext):
    user_text = message.text

    # Получаем IAM токен
    try:
        iam_token = get_iam_token()
        logger.info(f'Получен IAM-токен: {iam_token}')
    except requests.RequestException as e:
        logger.error(f'Ошибка при получении IAM-токена: {e}')
        await message.reply('Произошла ошибка при получении токена.')
        return

    # Отправляем запрос к Yandex GPT
    await message.answer(await send_request(iam_token, user_text), reply_markup=main_kb(message.from_user.id))
    await state.clear()
