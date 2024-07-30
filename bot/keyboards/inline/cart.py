from aiogram import types
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.models.cart import CartItem
from bot.keyboards.inline.category_kbd import MainCallback


def cart_keyboard(cart_items: list[CartItem] | None = None) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if cart_items:
        buttons = [types.InlineKeyboardButton(text=f"❌ {cart.artikul_id}", callback_data=f"del:{cart.artikul_id}") for cart in cart_items]
    
        builder.row(*buttons, width=1)
        
    builder.row(types.InlineKeyboardButton(text=_("✅ Buyurtma berish"), callback_data="order"))
    builder.row(types.InlineKeyboardButton(text=_("🗂 Buyurtmani davom ettirish"), callback_data=MainCallback(level=0).pack()))
    builder.row(types.InlineKeyboardButton(text=_("🧹 Tozalash"), callback_data="clear_cart"))
    
    return builder.as_markup()