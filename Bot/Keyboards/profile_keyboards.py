from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

profile_kb = InlineKeyboardMarkup(row_width=1)
profile_button1 = InlineKeyboardButton(text="💎 Мои подписки", callback_data="my_subscriptions")
profile_button2 = InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main_menu")
profile_kb.add(profile_button1, profile_button2)