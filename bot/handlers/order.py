from aiogram import Bot, types, Router, F
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.inline.group_order import accept_order_group
from bot.keyboards.inline.menu import main_keyboard
from bot.services.cart import clear_cart, get_cart_items
from bot.services.one_c import ONECClient
from bot.services.orders import add_order
from bot.services.users import get_manager, get_phone_number

router = Router(name="order")

@router.callback_query(F.data == "order")
async def order_handler(query: types.CallbackQuery, session: AsyncSession, bot: Bot) -> None:
    """Create order."""
    await query.answer()
    
    cart_items = await get_cart_items(session=session, user_id=query.from_user.id)
    
    if not cart_items:
        await query.answer(text=_("Savatcha bo'sh"))
        return
    
    order = await add_order(session=session, user_id=query.from_user.id, cart_items=cart_items)
    client_phone = await get_phone_number(session=session, user_id=query.from_user.id)
    manager = await get_manager(session=session, client_phone=client_phone)

    # Send to user that order has sent to Aiko manager    
    user_text = _("✅ Buyurtmangiz menejerga jo'natildi.\n")
    user_text += _("Buyurtma raqami: #{}\n\n").format(order.id)
    for item in cart_items:
        user_text += _("{}\n").format(item.name)
        user_text += _("Artikul: {}\n").format(item.artikul_id)
        user_text += _("Xarakteristika: <b>{}</b>\n").format(item.detail)
        user_text += _("{} * {:,.0f}$ = {:,.0f}$\n\n").format(item.quantity, item.price, item.price * item.quantity).replace(",", " ")

    await clear_cart(session=session, user_id=query.from_user.id)

    await query.message.edit_text(text=user_text)

    # Send to Aiko manager group about new order
    group_text = _("🆕 Yangi buyurtma\n")
    group_text += _("Ismi: {}\n").format(query.from_user.mention_html())
    group_text += _("username: @{}\n").format(query.from_user.username)
    group_text += _("Telefon raqami: {}\n").format(client_phone)
    
    group_text += user_text[user_text.find("\n")+1:]
    await bot.send_message(
        chat_id=-1002195162790,
        text=group_text,
        reply_markup=await accept_order_group(order_id=order.id),
    )

    # Create Order in 1C
    order_wood = []
    order_rattan = []
    
    general_data = {
            "name": f"{query.from_user.full_name} | {order.id} |",
            "phone": client_phone,
        }
    
    for item in cart_items:
        if item.brand == "wood":
            order_wood.append({
                "name": item.name,
                "artikul": item.artikul_id,
                "quantity": item.quantity,
                "price": float(item.price),
                "detail": item.detail,
                }
            )
        elif item.brand == "rattan":
            order_rattan.append({
                "name": item.name,
                "artikul": item.artikul_id,
                "quantity": item.quantity,
                "price": float(item.price),
                "detail": item.detail,
                }
            )

    if order_wood:
        general_data["order"] = order_wood
        api_client = ONECClient()
        async with api_client:
            if manager:
                await api_client.create_order(general_data, login=manager.login, password=manager.password, brand="wood")
            else:
                await api_client.create_order(general_data, brand="wood")

    if order_rattan:
        general_data["order"] = order_rattan
        api_client = ONECClient()
        async with api_client:
            if manager:
               await api_client.create_order(general_data, login=manager.login, password=manager.password, brand="rattan")
            else:
                await api_client.create_order(general_data, brand="wood")
    # Send to user
    await query.message.answer(
        text=_('Asosiy menu'),
        reply_markup=main_keyboard(),
    )
