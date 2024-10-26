from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

profile_kb = InlineKeyboardMarkup(row_width=1)
profile_button1 = InlineKeyboardButton(text="💎 Мои подписки", callback_data="my_subscriptions")
profile_button2 = InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main_menu")
profile_kb.add(profile_button1, profile_button2)

def create_subscriptions_keyboard(items, page: int = 0, items_per_page: int = 5):
    keyboard = InlineKeyboardMarkup(row_width=1)

    start_idx = page * items_per_page
    end_idx = start_idx + items_per_page

    for item in items[start_idx:end_idx]:
        keyboard.add(InlineKeyboardButton(text=item['text'], callback_data=item['callback_data']))

    if len(items) > items_per_page:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"subscriptions_page_{page - 1}"))
        if end_idx < len(items):
            nav_buttons.append(InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"subscriptions_page_{page + 1}"))
        if nav_buttons:
            keyboard.row(*nav_buttons)
    return keyboard