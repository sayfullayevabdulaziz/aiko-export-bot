from aiogram import Bot, types, Router, F
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.admin import AdminFilter
from bot.keyboards.inline.menu import main_keyboard
from bot.keyboards.inline.perm import UserStatusCallback
from bot.services.users import update_block

router = Router(name="user_status")

@router.callback_query(AdminFilter(), UserStatusCallback.filter())
async def user_status_handler(
    query: types.CallbackQuery, 
    callback_data: UserStatusCallback, 
    session: AsyncSession, 
    bot: Bot) -> None:
    """User Status."""
    await query.answer()
    
    if callback_data.action == "accept":
        await update_block(session=session, user_id=callback_data.user_id, is_block=False)
        await bot.send_message(
            chat_id=callback_data.user_id,
            text=_("Asosiy menu"),
            reply_markup=main_keyboard(),
        )

        status_text = _("✅ Yangi foydalanuvchiga ruxsat berdingiz.")
        text = status_text + query.message.text[49:]

        await query.message.edit_text(text=text)

    elif callback_data.action == "reject":
        await bot.send_message(
            chat_id=callback_data.user_id,
            text=_("Ruxsat berilmadi!"),
        )

        status_text = _("❌ Yangi foydalanuvchiga ruxsat berilmadi.")
        text = status_text + query.message.text[49:]

        await query.message.edit_text(text=text)
