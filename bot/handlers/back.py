from aiogram import types, Router, F
from aiogram.utils.i18n import gettext as _

from bot.keyboards.inline.menu import main_keyboard

router = Router(name="back")

@router.callback_query(F.data == "back_menu")
async def back_handler(query: types.CallbackQuery) -> None:
    """Return main menu."""
    await query.answer()
    await query.message.edit_text(
        text=_('Asosiy menu'),
        reply_markup=main_keyboard(),
    )