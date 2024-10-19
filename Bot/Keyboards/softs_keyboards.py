from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

softs_markup = InlineKeyboardMarkup(row_width=2)
softs_button1 = InlineKeyboardButton(text="🛠 Комбайн | TeleSkipper",callback_data="combine")
softs_button2 = InlineKeyboardButton(text="🗳 Модули",callback_data="combine_modules")
softs_button3 = InlineKeyboardButton(text="📒 Другое",callback_data="another_softs")
softs_button4 = InlineKeyboardButton(text="🔙 Назад",callback_data="back_to_main_menu")
softs_markup.add(softs_button1,softs_button2).add(softs_button3).add(softs_button4)