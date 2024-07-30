from aiogram import types, Router, F
from aiogram.utils.i18n import gettext as _
from bot.analytics.types import SubCategoryList, ProductList
from bot.handlers.product import product_handler
from aiogram.fsm.context import FSMContext
from bot.handlers.sub_category import sub_category_handler
from bot.keyboards.inline.finder_kbd import find_products_keyboard, FinderCallback, find_product_detail
from bot.services.one_c import ONECClient
from bot.services.get_image import AikoClient
from bot.states.finder import FinderState

router = Router(name="finder")

@router.callback_query(F.data == "finder")
async def finder_handler(query: types.CallbackQuery, state: FSMContext) -> None:
    """Finder input handler."""
    await query.answer()
    await state.set_state(FinderState.find)
    await query.message.edit_text(
        text=_("Mahsulot nomini kiriting"),
    )
    # await query.message.answer(text=_("Mahsulot nomini kiriting"), reply_markup=types.ReplyKeyboardRemove(),)


@router.message(FinderState.find)
async def get_product_name(message: types.Message, state: FSMContext):
    await state.update_data(product_name=message.text)
    product_name = message.text
    api_client = ONECClient()
    async with api_client:
        post_data = {
            "find": product_name,
        }
        post_response = await api_client.fetch_data(brand="wood", data=post_data, model=SubCategoryList)
        if not post_response.goods:
            post_response = await api_client.fetch_data(brand="rattan", data=post_data, model=SubCategoryList)
    
    if not post_response.goods:
        await message.reply(_("Mahsulot topilmadi"))
    else:
        await message.reply(_("Quyidagi mahsulotlardan birini tanlang"), reply_markup=find_products_keyboard(data=post_response.goods, msg=product_name))


async def get_product_name_from_callback(query: types.CallbackQuery, callback_data: FinderCallback):
    product_name = callback_data.msg
    api_client = ONECClient()
    async with api_client:
        post_data = {
            "find": product_name,
        }
        post_response = await api_client.fetch_data(brand="wood", data=post_data, model=SubCategoryList)
        if not post_response.goods:
            post_response = await api_client.fetch_data(brand="rattan", data=post_data, model=SubCategoryList)
    
    await query.message.edit_text(_("Quyidagi mahsulotlardan birini tanlang"), reply_markup=find_products_keyboard(data=post_response.goods, msg=product_name))



async def find_product_handler(query: types.CallbackQuery, callback_data: FinderCallback):
    """
        Get products by Category Code 
    """
    product_code = callback_data.product_code

    api_client = ONECClient()
    async with api_client:
        post_data = {
            "detail": product_code,
        }
        post_response = await api_client.fetch_data(post_data, model=ProductList)
    
    # _, products = await find_duplicate_codes(sub_category_list=post_response)
    async with AikoClient() as client:
        code = post_response.goods[0].DetailSiteCode
        img_url = await client.fetch_image_url(code=code[5:])
        discount_price = await client.extract_prices(code=code[5:])
        extract_url = await client.extract_href(code=code[5:])

    text = f"<b>{post_response.goods[0].name}</b>\n\n"
    for product in post_response.goods:
        text += _("Artikul: <b>{}</b>\n").format(product.DetailSiteCode)
        text += _("Xarakteristika: <b>{}</b>\n").format(product.Detail)
        text += _("Narxi: <b>{:,.0f} so`m</b>\n").format(product.prices).replace(",", " ")
        
        if discount_price:
            text += _("Chegirma narxi: <b>{} so`m</b>\n").format(discount_price.split("sum")[0])
        
        text += _("Qoldi: <b>{}</b>\n\n").format(product.stock)

    text += f"https://aiko.uz{extract_url}"

    await query.message.edit_text(
        text=text,
        reply_markup=find_product_detail(),
        link_preview_options=types.LinkPreviewOptions(
            url=f"https://aiko.uz{img_url.strip()}"
        )
    )
    await query.answer()



@router.callback_query(FinderCallback.filter())
async def finder_handler(query: types.CallbackQuery, callback_data: FinderCallback) -> None:
    """Category handler."""
    await query.answer()

    current_level = str(callback_data.level)
    levels = {
        "0": get_product_name_from_callback,
        "1": find_product_handler,
    }

    current_level_function = levels[current_level]

    await current_level_function(query, callback_data)