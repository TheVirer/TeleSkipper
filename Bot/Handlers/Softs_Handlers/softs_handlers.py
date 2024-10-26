import json
from Bot.bot import dp,bot
from aiogram import types
from Bot.Keyboards.softs_keyboards import softs_markup
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from Bot.Payments.CryptoBot import create_cryptobot_invoice,check_invoice
import aiofiles
from Database.database import add_soft_to_user, get_user_from_main_db
from datetime import datetime
from dateutil.relativedelta import relativedelta

@dp.callback_query_handler(lambda callback: callback.data == "softs",state="*")
async def softs_callback(callback: types.CallbackQuery, state: FSMContext):
    print((await get_user_from_main_db(user_id=callback.from_user.id)).softs)
    await state.finish()
    await bot.edit_message_reply_markup(message_id=callback.message.message_id,chat_id=callback.from_user.id,reply_markup=softs_markup)

@dp.callback_query_handler(lambda callback: callback.data == "combine")
async def combine_callback(callback: types.CallbackQuery):
    combine_info_text = """
some info about combine, maybe price
    """
    await bot.edit_message_caption(message_id=callback.message.message_id,caption=combine_info_text,chat_id=callback.from_user.id,parse_mode="HTML",reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="💸 Приобрести",callback_data="buy_combine"), InlineKeyboardButton(text="🔙 Назад",callback_data="softs")))

@dp.callback_query_handler(lambda callback: callback.data == "buy_combine")
async def buy_combine_callback(callback: types.CallbackQuery):
    await bot.edit_message_caption(message_id=callback.message.message_id,caption="⏳ <b>Выберите срок, на который хотите приобрести</b>",chat_id=callback.from_user.id,parse_mode="HTML",reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="⭐️ Навсегда | 75$",callback_data="combine_forever")).add(InlineKeyboardButton(text="✨ Месяц | 25$",callback_data="combine_month"),InlineKeyboardButton(text="🌟 3 Месяца | 49$",callback_data="combine_3months")).add(InlineKeyboardButton(text="🔙 Назад",callback_data="combine")))

@dp.callback_query_handler(lambda callback: callback.data.startswith("combine_"))
async def comb_callback(callback: types.CallbackQuery):
    await bot.edit_message_caption(message_id=callback.message.message_id,caption="🛒 <b>Выберите способ оплаты</b>",chat_id=callback.from_user.id,parse_mode="HTML",reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="💎 CryptoBot",callback_data=f"cryptobot_{callback.data}"), InlineKeyboardButton(text="🟢 Lolz Market",callback_data=f"lzt_{callback.data}"),InlineKeyboardButton(text="🔮 CrystalPay",callback_data=f"crystal_{callback.data}"),InlineKeyboardButton(text="🔙 Назад",callback_data="buy_combine")))

@dp.callback_query_handler(lambda callback: callback.data.startswith("cryptobot_"))
async def cryptobot_payment_callback(callback: types.CallbackQuery):
    async with aiofiles.open("Bot/to_buy_data.json","r",encoding="utf-8") as f:
        to_buy_data = json.loads(await f.read())

    buy_period = callback.data.split("_")[-1]
    soft = callback.data.split("_")[-2]

    invoice = await create_cryptobot_invoice(price=to_buy_data[soft]['periods'][buy_period]['price'])

    await bot.edit_message_caption(message_id=callback.message.message_id,caption="👇 Оплатите счет по кнопке ниже",chat_id=callback.from_user.id,parse_mode="HTML",reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="💸 Оплатить",url=invoice['url']), InlineKeyboardButton(text="✅ Проверить оплату",callback_data=f"ccbp_{soft}_{buy_period}_{invoice['id']}")).add(InlineKeyboardButton(text="❌ Отменить",callback_data="buy_combine")))

@dp.callback_query_handler(lambda callback: callback.data.startswith("ccbp_"))
async def check_cryptobot_payment(callback: types.CallbackQuery):
    invoice_id = callback.data.split("_")[-1]
    invoice_data = await check_invoice(invoice_id)
    if invoice_data.status != "paid":
        async with aiofiles.open("Bot/to_buy_data.json", "r", encoding="utf-8") as f:
            to_buy_data = json.loads(await f.read())
        soft_name = callback.data.split("_")[-3]
        buy_period = callback.data.split("_")[-2]

        license_exp = to_buy_data[soft_name]['periods'][buy_period]['license_exp']
        to_buy_data[soft_name]['soft_data']['exp_date'] = (datetime.now() + relativedelta(hours=license_exp['hours'],days=license_exp['days'],months=license_exp['months'],years=license_exp['years'])).strftime("%d.%m.%Y %H:%M")
        to_buy_data[soft_name]['soft_data']['name'] = to_buy_data[soft_name]['name']

        await add_soft_to_user(user_id=callback.from_user.id, soft_name=soft_name, soft_data=to_buy_data[soft_name]['soft_data'])
        await callback.answer()
    else:
        await callback.answer("❌ Оплата не обнаружена")