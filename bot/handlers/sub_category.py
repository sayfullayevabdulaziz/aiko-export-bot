from aiogram import types
from aiogram.utils.i18n import gettext as _
from bot.analytics.types import SubCategoryList
from bot.keyboards.inline.category_kbd import products_keyboard, MainCallback

from bot.services.one_c import ONECClient
from bot.utils.duplicate_sub_cat_code import find_duplicate_codes


async def sub_category_handler(query: types.CallbackQuery, callback_data: MainCallback):
    """
        Get products by Category Code 
    """
    category_code = callback_data.category_code

    api_client = ONECClient()
    async with api_client:
        post_data = {
            "code": category_code,
        }
        post_response = await api_client.fetch_data(post_data, model=SubCategoryList)
    
    products = await find_duplicate_codes(sub_category_list=post_response)

    await query.message.edit_text(
        text=_('Quyidagi mahsulotlardan birini tanlang'),
        reply_markup=products_keyboard(data=products, category_code=category_code, brand=callback_data.brand),
    )
    await query.answer()
