from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.i18n import gettext as _
from bot.analytics.types import CategoryList, SubCategory


class MainCallback(CallbackData, prefix="products"):
    level: int = 0
    brand: str | None = None
    category_code: str | None = None
    product_code: str | None = None
    

class NumberCallback(CallbackData, prefix="counter"):
    action: str
    price: int | None = None
    value: int | None = None
    artikul: str | None = None
    brand: str | None = None
    category_code: str | None = None
    max_qty: int | None = None


def category_keyboard(locale: str | None = None) -> InlineKeyboardMarkup:
    """Use in main menu."""
    level = 0
    
    buttons = [
        [InlineKeyboardButton(text="RATTAN", callback_data=MainCallback(level=level+1, brand="rattan").pack())],  # "cat_rattan")],
        [InlineKeyboardButton(text="WOOD", callback_data=MainCallback(level=level+1, brand="wood").pack())],
    ]
    buttons.append([InlineKeyboardButton(text=_("🛒 Korzina"), callback_data="cart")])
    buttons.append([InlineKeyboardButton(text=_("📂 Asosiy menu"), callback_data="back_menu")])

    keyboard = InlineKeyboardBuilder(markup=buttons)

    keyboard.adjust(2, 1)

    return keyboard.as_markup()


def sub_cat_keyboard(data: CategoryList, brand: str) -> InlineKeyboardMarkup:
    level = 1
    
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="📝 Прайс лист", callback_data=f"price_list:{brand}"))

    buttons = [InlineKeyboardButton(text=category.type, callback_data=MainCallback(level=level+1, brand=brand, category_code=category.code).pack()) 
               for category in data.goodstypes
            ]
    
    builder.row(*buttons, width=2)
    builder.row(InlineKeyboardButton(text=_("◀️ Orqaga"), callback_data=MainCallback(level=level-1).pack()))
    return builder.as_markup()


def products_keyboard(data: SubCategory, category_code: str, brand: str) -> InlineKeyboardMarkup:
    level = 2

    builder = InlineKeyboardBuilder()
    
    buttons = [InlineKeyboardButton(text=product.name, callback_data=MainCallback(level=level+1, brand=brand, category_code=category_code, product_code=product.code).pack()) 
               for product in data
            ]
    
    builder.row(*buttons, width=2)
    builder.row(InlineKeyboardButton(text=_("◀️ Orqaga"), callback_data=MainCallback(level=level-1, brand=brand).pack()))
    
    return builder.as_markup()


def product_detail(
        category_code: str, 
        brand: str, 
        artikuls: list[str], 
        cart: list[dict] | None = None,
) -> InlineKeyboardMarkup:
    level = 3

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
            InlineKeyboardButton(text="➖", callback_data=NumberCallback(
                action="change", 
                value=-1, 
                brand=brand, 
                category_code=category_code, 
                artikul=artikul_code["name"], 
                price=artikul_code["price"],
                max_qty=artikul_code["max_qty"],
            ).pack()),
            InlineKeyboardButton(text=str(artikul_code["quantity"]), callback_data=NumberCallback(action="show", artikul=artikul_code["name"]).pack()),
            InlineKeyboardButton(text="➕", callback_data=NumberCallback(
                action="change", 
                value=1, 
                brand=brand, 
                category_code=category_code, 
                artikul=artikul_code["name"], 
                price=artikul_code["price"],
                max_qty=artikul_code["max_qty"],
            ).pack()),
        )
        
    builder.adjust(1, 3, repeat=True)

    builder.row(InlineKeyboardButton(text=_("✅ Savatga qo'shish"), callback_data=NumberCallback(action="add_to_cart").pack()))
    builder.row(InlineKeyboardButton(text=_("◀️ Orqaga"), callback_data=MainCallback(level=level-1, brand=brand, category_code=category_code).pack()))
    return builder.as_markup()