from telebot import types
import emoji


def create_keyboard(keys, row_width=2, resize_keyboard=True, emojize=True):
    markup = types.ReplyKeyboardMarkup(
        row_width=row_width, resize_keyboard=resize_keyboard
    )
    if emojize:
        keys = list(map(emoji.emojize, keys))

    buttons = list(map(types.KeyboardButton, keys))

    markup.add(*buttons)
    return markup
