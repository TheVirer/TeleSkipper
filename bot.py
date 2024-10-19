from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot,storage=MemoryStorage())

from Bot.Handlers import *

def on_startup():
    print("Бот запущен")