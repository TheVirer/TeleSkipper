from Bot.bot import dp,bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import PROFILE_PIC
from Bot.Keyboards.profile_keyboards import profile_kb
from Bot.BotDatabase.users_database import get_user_from_bot_db
from Database.database import get_user_from_main_db
from Bot.Keyboards.profile_keyboards import create_subscriptions_keyboard

from datetime import datetime

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
    user = await get_user_from_main_db(user_id=callback.from_user.id)

    if user:
        softs = user.softs
        if softs != {}:
            print(softs)
            caption="<b>🧊 Используйте кнопки ниже</b>"

            items = []
            for soft in softs:
                text = softs[soft]['name']
                callback_data = soft
                items.append({"text" : text, "callback_data" : f"sub_{callback_data}"})

            markup = create_subscriptions_keyboard(items)

            await bot.edit_message_caption(chat_id=callback.from_user.id, message_id=callback.message.message_id, caption=caption, parse_mode="HTML", reply_markup=markup)

@dp.callback_query_handler(lambda callback: callback.data.startswith("sub_"))
async def get_subscription_info(callback: types.CallbackQuery):
    soft_name = callback.data.split("_")[-1]

    user = await get_user_from_main_db(user_id=callback.from_user.id)

    if user:
        softs = user.softs
        if user.softs != {}:
            try:
                soft_data = softs[soft_name]
            except:
                await callback.answer(text="🚫 Ошибка")
        else:
            await callback.answer(text="🚫 Ошибка")

        caption = f"""
⭐️ Подписка <code>{soft_data['name']}</code>
📆 {"Была активна" if datetime.strptime(soft_data['exp_date'], '%d.%m.%Y %H:%M') < datetime.now() else "Активна"} до <code>{soft_data['exp_date']}</code>
"""

        markup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="🔗 Изменить HWID", callback_data=f"changehwid_{soft_name}")).add(InlineKeyboardButton(text="⚙️ Настройка конфига", callback_data=f"config_{soft_name}")).add(InlineKeyboardButton(text="🔙 Назад", callback_data="profile"))

        await bot.edit_message_caption(chat_id=callback.from_user.id, message_id=callback.message.message_id, caption=caption, parse_mode="HTML", reply_markup=markup)
    else:
        await callback.answer(text="🚫 Ошибка")
