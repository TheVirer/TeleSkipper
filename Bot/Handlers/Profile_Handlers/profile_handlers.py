from bot import dp,bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import PROFILE_PIC

@dp.callback_query_handler(lambda callback: callback.data == "profile", state="*")
async def profile(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id, media=types.InputMediaPhoto(photo=PROFILE_PIC), reply_markup=None)