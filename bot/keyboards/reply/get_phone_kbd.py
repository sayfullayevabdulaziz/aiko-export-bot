from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _


async def register_btn(locale: str = None) -> ReplyKeyboardMarkup:
    btn = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=_('Telefon raqam kiritish', locale=locale), request_contact=True)
        ],
    ],
        resize_keyboard=True,
        input_field_placeholder=_("Telefon raqamingizni kiriting.", locale=locale)
    )
    return btn