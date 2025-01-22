from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Случайная шутка", callback_data="random_joke")],
        [InlineKeyboardButton("Популярный GIF", callback_data="trending_gif")]
                                                ]
    )