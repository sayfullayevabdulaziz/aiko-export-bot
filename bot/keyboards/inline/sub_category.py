from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from bot.analytics.types import CategoryList


class SubCategoryCallback(CallbackData, prefix="sub_category"):
    code: str


def sub_cat_keyboard(data: CategoryList) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=category.type, callback_data=SubCategoryCallback(code=category.code).pack()) 
               for category in data.goodstypes
            ]
    
    builder.row(*buttons, width=2)
    return builder.as_markup()