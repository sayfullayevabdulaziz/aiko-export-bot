from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class UserStatusCallback(CallbackData, prefix="user_status"):
    action: str
    user_id: int


async def permission_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Use in main menu."""
    buttons = [
        [InlineKeyboardButton(text=_("✅ Ruxsat berish"), callback_data=UserStatusCallback(
            action="accept", 
            user_id=user_id).pack())
            ],
        [InlineKeyboardButton(text=_("❌ Rad qilish"), callback_data=UserStatusCallback(
            action="reject", 
            user_id=user_id).pack())
            ],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    return keyboard.as_markup()
