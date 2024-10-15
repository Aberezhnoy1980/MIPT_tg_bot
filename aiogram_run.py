import asyncio
from create_bot import bot, dp, scheduler
from handlers.start import start_router
from handlers.reg import reg_router
from handlers.moex_handler import stock_router
from handlers.about_handler import about_router
from handlers.ygpt_handler import ygpt_router


# from work_time.time_func import send_time_msg

async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_router(start_router)
    dp.include_router(reg_router)
    dp.include_router(stock_router)
    dp.include_router(about_router)
    dp.include_router(ygpt_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
