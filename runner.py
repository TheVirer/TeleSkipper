from Bot.bot import dp, on_startup
import asyncio
from Bot.BotDatabase.users_database import create_db as create_bot_db
from Database.database import create_db as create_main_db
from API.api import run_api
from concurrent.futures import ThreadPoolExecutor

async def start_dp(dp, on_startup):
    on_startup()
    await dp.skip_updates()
    await dp.start_polling()

async def run_api_in_thread():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, run_api)

async def main():
    tasks = [
        asyncio.create_task(create_main_db()),
        asyncio.create_task(create_bot_db()),
        asyncio.create_task(start_dp(dp,on_startup=on_startup)),
        asyncio.create_task(run_api_in_thread())
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())