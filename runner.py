from aiogram import executor
from bot import dp, on_startup
import asyncio
from Bot.users_database import create_db as create_bot_db
from Database.database import create_db as create_main_db

async def start_dp(dp, on_startup):
    on_startup()
    await dp.skip_updates()
    await dp.start_polling()

async def main():
    tasks = [
        asyncio.create_task(create_main_db()),
        asyncio.create_task(create_bot_db()),
        asyncio.create_task(start_dp(dp,on_startup=on_startup))
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())