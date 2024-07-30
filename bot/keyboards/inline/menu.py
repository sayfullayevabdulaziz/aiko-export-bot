from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.inline.category_kbd import MainCallback


def main_keyboard(locale: str | None = None) -> InlineKeyboardMarkup:
    """Use in main menu."""
    buttons = [
        [InlineKeyboardButton(text=_("🔍 Qidirish", locale=locale), switch_inline_query_current_chat="")],
        [InlineKeyboardButton(text=_("🗂 Kategoriya", locale=locale), callback_data=MainCallback(level=0).pack())],
        [InlineKeyboardButton(text=_("🛒 Korzina", locale=locale), callback_data="cart")],
        [InlineKeyboardButton(text=_("🔥 Katalog", locale=locale), callback_data="catalogue")],
        [InlineKeyboardButton(text=_("ℹ️ Info", locale=locale), callback_data="about")],
        [InlineKeyboardButton(text=_("🌎 Tilni o'zgartirish", locale=locale), callback_data="change-lang")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    keyboard.adjust(1,1,2)

    return keyboard.as_markup()
