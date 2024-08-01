from aiogram import types, Router, F
from aiogram.utils.i18n import gettext as _

from bot.keyboards.inline.menu import main_keyboard

router = Router(name="catalogue")

@router.callback_query(F.data == "catalogue")
async def back_handler(query: types.CallbackQuery) -> None:
    """Return main menu."""
    await query.answer()
    await query.message.answer_document(document="BQACAgIAAxkBAAOTZqtmlECAc_mwMhMR19R-s8xkopsAAodNAAJXGmFJsPu7BJ5hL341BA")
