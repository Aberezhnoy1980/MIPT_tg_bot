from aiogram import Router, F
from aiogram.types import Message
from keyboards.all_kb import github_btn

about_router = Router()


@about_router.message(F.text == '📖 О проекте')
async def cmd_catalog(message: Message):
    await message.answer(
        '''Небольшой академический проект магистратуры "Финансовые технологии. Разработка и аналитика" МФТИ. 
        Возможно, в своем развитии, мини проект ляжет в основу диссертации или вырастет в полноценный сервис. 
        Приглашаю всех желающих принять участие''',
        reply_markup=github_btn().as_markup())