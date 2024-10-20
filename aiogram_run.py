import asyncio
from create_bot import bot, dp, scheduler
from handlers.start import start_router
from handlers.reg import reg_router
from handlers.securities_handler import stock_router
from handlers.portfolio_handler import portfolio_router
from handlers.about_handler import about_router
from handlers.ygpt_handler import ygpt_router
from handlers.currency_handler import currency_router
from utils.commands import start_bot, stop_bot


# from work_time.time_func import send_time_msg

async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_routers(
        start_router,
        reg_router,
        stock_router,
        portfolio_router,
        currency_router,
        ygpt_router,
        about_router
    )
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
