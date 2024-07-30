from aiogram import types, Router, F
from aiogram.utils.i18n import gettext as _
from bot.analytics.types import CategoryList
from bot.handlers.product import product_handler
from bot.handlers.sub_category import sub_category_handler
from bot.keyboards.inline.category_kbd import MainCallback, category_keyboard, sub_cat_keyboard, products_keyboard, product_detail
from bot.services.one_c import ONECClient

router = Router(name="category")

# @router.callback_query(F.data == "category")
async def category_handler(query: types.CallbackQuery, callback_data: MainCallback) -> None:
    """Category handler."""
    await query.answer()
    await query.message.edit_text(text=_("Quyidagi birini tanlang"), reply_markup=category_keyboard(),)





# if callback_data.brand == "rattan":
#     await query.answer(text=_("Tez kunda mahsulotlar qo'shiladi"), show_alert=True)
#     # await query.message.edit_text(
#     #     text=_('Asosiy menu'),
#     #     reply_markup=main_keyboard(),
#     # )
# else:
#     api_client = ONECClient()
#     async with api_client:
#         post_data = {
#             "type": "goods",
#         }
#         post_response = await api_client.fetch_data(post_data, model=CategoryList)
    

#     await query.message.edit_text(
#         text=_('Quyidagi kategoriyalardan birini tanlang'),
#         reply_markup=sub_cat_keyboard(data=post_response),
#     )


# @router.callback_query(F.data.startswith("cat_"))
async def category_rattan_wood_handler(query: types.CallbackQuery, callback_data: MainCallback) -> None:
    """Category Wood, Rattan handler."""
    # await query.answer(text=_("Tez kunda mahsulotlar qo'shiladi"), show_alert=True)
    # await query.message.edit_text(
    #     text=_('Asosiy menu'),
    #     reply_markup=main_keyboard(),
    # )
    # action = query.data.split("_")[1]

    if callback_data.brand == "rattan":
        api_client = ONECClient()
        async with api_client:
            post_data = {
                "type": "goods",
            }
            post_response = await api_client.fetch_data(brand="rattan", data=post_data, model=CategoryList)
        

        await query.message.edit_text(
            text=_('Quyidagi kategoriyalardan birini tanlang'),
            reply_markup=sub_cat_keyboard(data=post_response, brand=callback_data.brand),
        )
        
    elif callback_data.brand == "wood":
        api_client = ONECClient()
        async with api_client:
            post_data = {
                "type": "goods",
            }
            post_response = await api_client.fetch_data(brand="wood", data=post_data, model=CategoryList)
        

        await query.message.edit_text(
            text=_('Quyidagi kategoriyalardan birini tanlang'),
            reply_markup=sub_cat_keyboard(data=post_response, brand=callback_data.brand),
        )


@router.callback_query(MainCallback.filter())
async def final_handler(query: types.CallbackQuery, callback_data: MainCallback) -> None:
    """Category handler."""
    await query.answer()

    current_level = str(callback_data.level)
    levels = {
        "0": category_handler,
        "1": category_rattan_wood_handler,
        "2": sub_category_handler,
        "3": product_handler,
    }

    current_level_function = levels[current_level]

    await current_level_function(query, callback_data)