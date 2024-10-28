from Bot.bot import dp,bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import PROFILE_PIC
from Bot.States.ChangeHWIDStates import HWIDChangeForm
from Bot.Keyboards.profile_keyboards import profile_kb
from Bot.BotDatabase.users_database import get_user_from_bot_db
from Database.database import get_user_from_main_db, change_hwid_by_id, check_hwid_for_availability, add_hwid_entry, get_hwid_by_id_for_soft
from Bot.Keyboards.profile_keyboards import create_subscriptions_keyboard
import re

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
        else:
            await callback.answer(text="❗️ У вас еще нет подписок")

@dp.callback_query_handler(lambda callback: callback.data.startswith("sub_"), state="*")
async def get_subscription_info(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()

    soft_name = callback.data.split("_")[-1]

    user = await get_user_from_main_db(user_id=callback.from_user.id)

    if user:
        softs = user.softs
        if user.softs != {}:
            try:
                soft_data = softs[soft_name]
            except:
                await callback.answer(text="🚫 Ошибка")
                return
        else:
            await callback.answer(text="🚫 Ошибка")
            return

        presence_of_binding = await get_hwid_by_id_for_soft(user_id=callback.from_user.id, soft=soft_name)

        caption = f"""
⭐️ Подписка <code>{soft_data['name']}</code>
📆 {"Была активна до" if datetime.strptime(soft_data['exp_date'], '%d.%m.%Y %H:%M') < datetime.now() else "Активна"} до <code>{soft_data['exp_date']}</code>
🔗 HWID: <code>{presence_of_binding.hwid if presence_of_binding is not None else "не привязан"}</code>
"""

        markup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="🔗 Изменить HWID", callback_data=f"changehwid_{soft_name}")).add(InlineKeyboardButton(text="⚙️ Настройка конфига", callback_data=f"config_{soft_name}")).add(InlineKeyboardButton(text="🔙 Назад", callback_data="profile"))
        try:
            await bot.edit_message_caption(chat_id=callback.from_user.id, message_id=callback.message.message_id, caption=caption, parse_mode="HTML", reply_markup=markup)
        except:
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            await bot.send_photo(chat_id=callback.from_user.id, photo=PROFILE_PIC, caption=caption, parse_mode="HTML", reply_markup=markup)
    else:
        await callback.answer(text="🚫 Ошибка")


@dp.callback_query_handler(lambda callback: callback.data.startswith("changehwid_"), state="*")
async def change_hwid(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()

    soft_name = callback.data.split("_")[-1]

    await HWIDChangeForm.HWID.set()
    await state.update_data(soft_name=soft_name)
    await bot.edit_message_caption(chat_id=callback.from_user.id, message_id=callback.message.message_id, caption="🔗 Введите новый HWID", reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="🔙 Назад", callback_data=f"sub_{soft_name}")))

@dp.message_handler(content_types=types.ContentType.TEXT, state=HWIDChangeForm.HWID)
async def confirm_changing_hwid(message: types.Message, state: FSMContext):
    hwid_value = message.text
    data = await state.get_data()
    soft_name = data["soft_name"]

    await bot.send_message(chat_id=message.from_user.id, text=f"❓ Вы точно хотите сменить HWID?\nВведенные данные: <b>{hwid_value}</b>", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="✅ Сменить", callback_data=f"chwid_{hwid_value}")).add(InlineKeyboardButton(text="❌ Отмена", callback_data=f"sub_{soft_name}")))

@dp.callback_query_handler(lambda callback: callback.data.startswith("chwid_"), state=HWIDChangeForm.HWID)
async def change_hwid_in_db(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    soft_name = data["soft_name"]

    await state.finish()

    hwid_value = callback.data.split("_")[-1].lower()

    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text="⌛️ Перевязываем...")

    hwid_pattern = re.compile(r'^[A-Fa-f0-9]{8}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{12}$')

    if hwid_pattern.match(hwid_value):
        checked_hwid = await check_hwid_for_availability(hwid=hwid_value, soft=soft_name)
        if checked_hwid is not None:
            if checked_hwid.user_id == callback.from_user.id:
                if checked_hwid.soft != soft_name:
                    await change_hwid_by_id(user_id=callback.from_user.id, soft=soft_name, hwid=hwid_value)

                    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,text="🔗 HWID успешно перевязан!",reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="🔙 Вернуться", callback_data=f"sub_{soft_name}")))
                else:
                    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text="❌ У вас уже привязан этот HWID")
            else:
                await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,text="❌ Вы не сможете привязать этот HWID")
        else:
            await change_hwid_by_id(user_id=callback.from_user.id, soft=soft_name, hwid=hwid_value)

            await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,text="🔗 HWID успешно привязан!",reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="🔙 Вернуться", callback_data=f"sub_{soft_name}")))
    else:
        await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,text="❌ Недопустимое значение\n\n❓ Узнайте свой HWID с помощью команды:\n<code>wmic csproduct get uuid</code>", parse_mode="HTML")