from Bot.bot import dp
from aiogram import types
from aiogram.dispatcher import FSMContext

@dp.callback_query_handler(lambda callback: callback.data == "info", state="*")
async def info(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()

    caption = """
text
    """

