from Bot.bot import bot,dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from Bot.BotDatabase.users_database import get_user_from_bot_db,add_user_to_bot_database
from Bot.Keyboards.main_keyboards import main_markup
from Database.database import add_user_to_main_database, get_user_from_main_db

from datetime import datetime

@dp.message_handler(commands="start", state="*")
async def start_command(message: types.Message, state: FSMContext):
    if not await get_user_from_bot_db(user_id=message.from_user.id):
        await add_user_to_bot_database(user_id=message.from_user.id,first_name=message.from_user.first_name,username=message.from_user.username,reg_data=datetime.now().strftime("%d-%m-%Y"))
    if not await get_user_from_main_db(user_id=message.from_user.id):
        await add_user_to_main_database(user_id=message.from_user.id,first_name=message.from_user.first_name)

    await bot.send_photo(photo="https://media.discordapp.net/attachments/791233572458594324/1293224335431045192/main-menu.png?ex=67069884&is=67054704&hm=8b39339be20befce0b1ae83251af2d99dee1b5ca13576683c004367a18166cf6&=&format=webp&quality=lossless&width=1505&height=902",caption="🧊 <b>Используйте кнопки ниже</b>",chat_id=message.from_user.id,parse_mode="HTML",reply_markup=main_markup)
    await state.finish()

@dp.callback_query_handler(lambda callback: callback.data == "back_to_main_menu", state="*")
async def back_to_main_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_media(message_id=callback.message.message_id,media=types.InputMediaPhoto("https://media.discordapp.net/attachments/791233572458594324/1293224335431045192/main-menu.png?ex=67069884&is=67054704&hm=8b39339be20befce0b1ae83251af2d99dee1b5ca13576683c004367a18166cf6&=&format=webp&quality=lossless&width=1505&height=902",caption="🧊 <b>Используйте кнопки ниже</b>",parse_mode="HTML"),chat_id=callback.from_user.id,reply_markup=main_markup)
    await state.finish()