from aiogram import types
from aiogram.utils.i18n import gettext as _


def back_keyboard() -> types.InlineKeyboardMarkup:
    
    buttons = [
        [types.InlineKeyboardButton(text=_("◀️ Menyuga"), callback_data="back_menu")]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard