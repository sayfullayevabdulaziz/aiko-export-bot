from contextlib import suppress
from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from bot.cache.redis import get_product_with_pipeline
from bot.keyboards.inline.cart import cart_keyboard
from bot.keyboards.inline.category_kbd import NumberCallback, category_keyboard, product_detail
from bot.keyboards.inline.menu import main_keyboard
from bot.services.cart import clear_cart, get_cart_items, upsert_cart_item, delete_from_cart
from bot.utils.cart import ShoppingCart


router = Router(name="cart-items")


@router.callback_query(F.data.startswith("del:"))
async def delete_one_item(query: types.CallbackQuery, session: AsyncSession) -> None:
    await query.answer()

    artikul = query.data.split(":")[1]
    await delete_from_cart(session=session, user_id=query.from_user.id, artikul=artikul)
    # asyncio.sleep(0.001)
    cart_items = await get_cart_items(session=session, user_id=query.from_user.id)

    if not cart_items:
        await query.message.edit_text(
            text=_("Savatcha bo'sh"),
            reply_markup=cart_keyboard(),
        )
        return

    text = _("Savatcha:\n\n")
    for item in cart_items:
        text += _("{}\n").format(item.name)
        text += _("Artikul: {}\n").format(item.artikul_id)
        text += _("{} * {:,.0f}$ = {:,.0f}$\n\n").format(item.quantity, item.price, item.price * item.quantity).replace(",", " ")

    await query.message.edit_text(
        text=text,
        reply_markup=cart_keyboard(cart_items=cart_items),
    )


@router.callback_query(F.data == "clear_cart")
async def clear_cart_items(query: types.CallbackQuery, session: AsyncSession) -> None:
    """Return main menu."""
    await query.answer()
    user_cart = ShoppingCart(user_id=query.from_user.id)
    
    await clear_cart(session=session, user_id=query.from_user.id)
    await user_cart.clear_cart_from_redis()
    
    await query.message.edit_text(
        text=_("Savatcha tozalandi"),
        reply_markup=main_keyboard(),
    )


@router.callback_query(F.data == "cart")
async def cart_handler(query: types.CallbackQuery, session: AsyncSession) -> None:
    """Return main menu."""
    await query.answer()

    cart_items = await get_cart_items(session=session, user_id=query.from_user.id)

    if not cart_items:
        await query.message.edit_text(
            text=_("Savatcha bo'sh"),
            reply_markup=cart_keyboard(),
        )
        return

    text = _("Savatcha:\n\n")
    for item in cart_items:
        text += _("{}\n").format(item.name)
        text += _("Artikul: {}\n").format(item.artikul_id)
        text += _("{} * {:,.0f}$ = {:,.0f}$\n\n").format(item.quantity, item.price, item.price * item.quantity).replace(",", " ")

    await query.message.edit_text(
        text=text,
        reply_markup=cart_keyboard(cart_items=cart_items),
    )


async def update_num_text_fab(message: types.Message, callback_data, cart: ShoppingCart):
    with suppress(TelegramBadRequest):
        product = await get_product_with_pipeline(user_id=message.chat.id)
        img_url = product["img_url"]
        artikuls = product["artikuls"]
        # quantity = cart[message.chat.id]
        # print("AVC123 -> ", quantity)
        text = product["text"]

        await message.edit_text(
            text=text,
            reply_markup=product_detail(
                category_code=callback_data.category_code, 
                brand=callback_data.brand,
                artikuls=artikuls,
                cart=await cart.get_items()
            ),
            link_preview_options=types.LinkPreviewOptions(
                url=f"https://aiko.uz{img_url.strip()}" if img_url else None,
            )
        )


@router.callback_query(NumberCallback.filter())
async def counter_handler(query: types.CallbackQuery, callback_data: NumberCallback, session: AsyncSession) -> None:
    user_shopping_cart = ShoppingCart(user_id=query.from_user.id)
    if callback_data.action == "change":

        quantity, _p = await user_shopping_cart.get_item(item_id=callback_data.artikul)

        if quantity is not None:
            quantity += callback_data.value

            if quantity <= 0:
                await user_shopping_cart.remove_item(item_id=callback_data.artikul)
                await update_num_text_fab(query.message, callback_data, cart=user_shopping_cart)
            elif quantity <= callback_data.max_qty:
                await user_shopping_cart.add_item(item_id=callback_data.artikul, quantity=quantity, price=callback_data.price)
                await update_num_text_fab(query.message, callback_data, cart=user_shopping_cart)
        else:
            if callback_data.value > 0:
                await user_shopping_cart.add_item(item_id=callback_data.artikul, quantity=callback_data.value, price=callback_data.price)
                await update_num_text_fab(query.message, callback_data, cart=user_shopping_cart)


    elif callback_data.action == "add_to_cart":
        text = query.message.text
        product_name = text.split("\n")[0]

        user_carts = await user_shopping_cart.get_items()
        await upsert_cart_item(session=session, 
                               user_id=query.from_user.id,
                               cart_items=user_carts,
                               product_name=product_name,
                            )
    
        await query.message.edit_text(
            text=_("Savatga qo'shildi"),
            reply_markup=category_keyboard(),
        )
        await user_shopping_cart.clear_cart_from_redis()
    else:
        await query.answer(text=callback_data.value, show_alert=True)