from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from bot.analytics.types import SubCategory


class ProductCallback(CallbackData, prefix="products"):
    code: str


def products_keyboard(data: SubCategory) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=product.name, callback_data=ProductCallback(code=product.code).pack()) 
               for product in data
            ]
    
    builder.row(*buttons, width=2)
    return builder.as_markup()