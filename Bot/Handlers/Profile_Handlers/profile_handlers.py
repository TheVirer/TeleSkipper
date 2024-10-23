from Bot.bot import dp,bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import PROFILE_PIC
from Bot.Keyboards.profile_keyboards import profile_kb
from Database.database import get_user_from_main_db

@dp.callback_query_handler(lambda callback: callback.data == "profile", state="*")
async def profile(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()

    user = get_user_from_main_db(user_id=callback.from_user.id)

    if user:
        profile_text = f"""
🆔 Telegram ID: {user.user_id}
⏳ Дата регистрации: 
"""
        await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id, media=types.InputMediaPhoto(media=PROFILE_PIC, caption=profile_text, parse_mode="HTML"), reply_markup=profile_kb)
    else:
        await callback.answer(text="🚫 Ошибка доступа")