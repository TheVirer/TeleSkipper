from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

main_markup = InlineKeyboardMarkup(row_width=2)
main_button1 = InlineKeyboardButton(text="👤 Профиль",callback_data="profile")
main_button2 = InlineKeyboardButton(text="💰 Приобрести доступ",callback_data="softs")
main_button3 = InlineKeyboardButton(text="🕰 Тестовый период",callback_data="test_period")
main_button4 = InlineKeyboardButton(text="ℹ️ Информация",callback_data="info")
main_markup.add(main_button1).add(main_button2,main_button3).add(main_button4)