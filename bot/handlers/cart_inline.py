from contextlib import suppress
from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from bot.cache.redis import get_product_with_pipeline
from bot.keyboards.inline.category_kbd import category_keyboard
from bot.keyboards.inline.inline_query_kbd import NumberInlineCallback, product_detail_for_inline
from bot.services.cart import upsert_cart_item
from bot.utils.cart import ShoppingCart


router = Router(name="inline-cart-items")


async def update_num_text_fab(message: types.Message, callback_data, cart: ShoppingCart):
    with suppress(TelegramBadRequest):
        product = await get_product_with_pipeline(user_id=message.chat.id)
        code = product["code"]
        img_url = product["img_url"]
        artikuls = product["artikuls"]
        # quantity = cart[message.chat.id]
        # print("AVC123 -> ", quantity)
        text = product["text"]

        await message.edit_text(
            text=text,
            reply_markup=product_detail_for_inline(
                artikuls=artikuls,
                cart=await cart.get_items()
            ),
            link_preview_options=types.LinkPreviewOptions(
                url=f"https://aiko.uz{img_url.strip()}" if img_url else None,
            )
        )


@router.callback_query(NumberInlineCallback.filter())
async def inline_counter_handler(query: types.CallbackQuery, callback_data: NumberInlineCallback, session: AsyncSession) -> None:
    # await upsert_cart_item(session=session, user_id=query.from_user.id, artikul_id="test", quantity=1)
    user_shopping_cart = ShoppingCart(user_id=query.from_user.id)
    if callback_data.action == "change":
        # await update_num_text_fab(callback.message, user_value + callback_data.value)
        # callback_data.summ = callback_data.summ + callback_data.value
        # quantity = 0
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