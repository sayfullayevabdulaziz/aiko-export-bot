from aiogram import types
from aiogram.utils.i18n import gettext as _


async def accept_order_group(order_id: str) -> types.InlineKeyboardMarkup:
    
    buttons = [
        [types.InlineKeyboardButton(text=_("✅ Qabul qilish"), callback_data=f"accepted_order:{order_id}")],
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard