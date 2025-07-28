import asyncio
import os
from aiogram import Dispatcher, Bot
from dotenv import load_dotenv

from app.handlers import router, init_models

async def main():
    load_dotenv()
    dp = Dispatcher()
    bot = Bot(token=os.getenv('TG_TOKEN'))
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_router(router)
    model, searcher = await init_models()
    setattr(bot, "model", model)
    setattr(bot, "searcher", searcher)
    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    print('Бот запущен')

async def shutdown(dispatcher: Dispatcher):
    print('Бот остановлен')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass