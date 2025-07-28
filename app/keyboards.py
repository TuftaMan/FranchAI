from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Задать вопрос', callback_data='question')],
    [InlineKeyboardButton(text='О нас', callback_data='about')]
])

call_to_operator = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Связаться с опертором', callback_data='call_operator')],
    [InlineKeyboardButton(text='Задать еще один вопрос', callback_data='question')],
    [InlineKeyboardButton(text='Главное меню', callback_data='back_to_menu')]
])

back_to_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Главное меню', callback_data='back_to_menu')]
])