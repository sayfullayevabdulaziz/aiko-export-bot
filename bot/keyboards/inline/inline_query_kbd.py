from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.i18n import gettext as _


class NumberInlineCallback(CallbackData, prefix="inline-counter"):
    action: str
    price: int | None = None
    value: int | None = None
    artikul: str | None = None
    max_qty: int | None = None


def product_detail_for_inline( 
        artikuls: list[str], 
        cart: list[dict] | None = None,
) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()
    for artikul_code in artikuls:
        builder.row(InlineKeyboardButton(text=f"{artikul_code['name']}({artikul_code['detail']})", callback_data="nothing"))
        if cart:
            for artikul, quantity_price in cart.items():
                if artikul_code["name"] == artikul:
                    # if quantity < 0:
                    #     artikul_code["quantity"] = 0
                    artikul_code["quantity"] = quantity_price['quantity']

        builder.add(
            InlineKeyboardButton(text="➖", callback_data=NumberInlineCallback(
                action="change", 
                value=-1, 
                artikul=artikul_code["name"], 
                price=artikul_code["price"],
                max_qty=artikul_code["max_qty"],
            ).pack()),
            InlineKeyboardButton(text=str(artikul_code["quantity"]), callback_data=NumberInlineCallback(action="show", artikul=artikul_code["name"]).pack()),
            InlineKeyboardButton(text="➕", callback_data=NumberInlineCallback(
                action="change", 
                value=1, 
                artikul=artikul_code["name"], 
                price=artikul_code["price"],
                max_qty=artikul_code["max_qty"],
            ).pack()),
        )
        
    builder.adjust(1, 3, repeat=True)

    builder.row(InlineKeyboardButton(text=_("✅ Savatga qo'shish"), callback_data=NumberInlineCallback(action="add_to_cart").pack()))
    builder.row(InlineKeyboardButton(text=_("◀️ Menyuga"), callback_data="back_menu"))
    return builder.as_markup()