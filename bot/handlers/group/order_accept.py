from datetime import datetime
from aiogram import Bot, types, Router, F
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

# from bot.filters.chat_type import ChatTypeFilter
from bot.services.orders import get_user_id_by_order_id, update_order_status
from bot.services.users import get_phone_number

router = Router()


@router.callback_query(F.data.startswith("accepted_order:"))
async def accept_order(query: types.CallbackQuery, session: AsyncSession, bot: Bot) -> None:
    await query.answer()

    order_id = query.data.split(":")[1]

    await update_order_status(session=session, order_id=order_id, accepted_user_id=query.from_user.id)
    old_text = query.message.text
    
    text = _("✅ Buyurtma qabul qilindi\n")
    text += _("Kim tomonidan: {}\n").format(query.from_user.mention_html())
    text += _("Qabul qilingan vaqt: {}\n\n").format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    text += _("#Zakaz")

    text += old_text[old_text.find("\n"):]

    await query.message.edit_text(
        text=text,
    )

    # Send to user that order was accepted
    phone = await get_phone_number(session=session, user_id=query.from_user.id)
    
    user_id = await get_user_id_by_order_id(session=session, order_id=order_id)
    user_text = _("✅ Buyurtmangiz qabul qilindi.\n\n")
    user_text += _("Buyurtma raqami: #{}\n").format(order_id)
    user_text += _("Kim tomonidan: {}\n").format(query.from_user.mention_html())
    user_text += _("username: @{}\n").format(query.from_user.username)
    user_text += _("Telefon raqami: {}\n").format(phone)
    user_text += _("Qabul qilingan vaqt: {}\n").format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    await bot.send_message(
        chat_id=user_id,
        text=user_text,
    )