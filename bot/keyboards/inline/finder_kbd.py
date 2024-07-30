from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.i18n import gettext as _
from bot.analytics.types import CategoryList, SubCategoryList


class FinderCallback(CallbackData, prefix="finder"):
    level: int = 0
    msg: str | None = None
    product_code: str | None = None
    

def find_products_keyboard(data: SubCategoryList, msg: str) -> InlineKeyboardMarkup:
    level = 0

    builder = InlineKeyboardBuilder()
    
    buttons = [InlineKeyboardButton(text=product.name, callback_data=FinderCallback(level=level+1, product_code=product.code, msg=msg).pack()) 
               for product in data
            ]
    
    builder.row(*buttons, width=2)
    builder.row(InlineKeyboardButton(text=_("Asosiy menu"), callback_data="back_menu"))
    
    return builder.as_markup()


def find_product_detail() -> InlineKeyboardMarkup:
    level = 1

    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text=_("Orqaga"), callback_data=FinderCallback(level=level-1).pack()))
    return builder.as_markup()