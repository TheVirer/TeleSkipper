from Bot.bot import dp,bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import PROFILE_PIC
from Bot.Keyboards.profile_keyboards import profile_kb
from Bot.BotDatabase.users_database import get_user_from_bot_db
from Database.database import get_user_from_main_db

@dp.callback_query_handler(lambda callback: callback.data == "profile", state="*")
async def profile(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()

    user = await get_user_from_bot_db(user_id=callback.from_user.id)

    if user:
        profile_text = f"""
🆔 Telegram ID: <code>{user.user_id}</code>
⏳ С нами с: <code>{user.reg_data}</code>
"""
        await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id, media=types.InputMediaPhoto(media=PROFILE_PIC, caption=profile_text, parse_mode="HTML"), reply_markup=profile_kb)
    else:
        await callback.answer(text="🚫 Ошибка доступа")

@dp.callback_query_handler(lambda callback: callback.data == "my_subscriptions")
async def get_subscriptions(callback: types.CallbackQuery):
    print(1543)
    user = await get_user_from_main_db(user_id=callback.from_user.id)

    if user:
        print(user)
        text="<b>📦 Ваши подписки:</b>"

        softs = json.loads(user.softs)
        if softs:
            names = [data['name'] for key, data in softs.items()]
            print("Список найденных имен:", names)
        else:
            print("Софт не найден.")
    else:
        print("huy")