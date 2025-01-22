from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Случайная шутка", callback_data="random_joke")],
        [InlineKeyboardButton(text="Популярный GIF", callback_data="trending_gif")]
                                                ]
    )