from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

profile_kb = InlineKeyboardMarkup(row_width=1)
profile_button1 = InlineKeyboardButton(text="💎 Мои подписки", callback_data="my_subscriptions")