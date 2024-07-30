from aiogram import Router, types, F
from aiogram.utils.i18n import gettext as _


from bot.keyboards.inline.language import language_keyboard

router = Router(name="change_language")


@router.callback_query(F.data == "change-lang")
async def change_language_handler(query: types.CallbackQuery) -> None:
    """Change UI language"""
    await query.answer()

    text = _("Ma'lumotlarni qaysi tilda qabul qilmoqchisiz?")

    await query.message.edit_text(
        text=text,
        reply_markup=language_keyboard()
    )
