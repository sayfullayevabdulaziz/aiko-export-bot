from aiogram import types
from aiogram.utils.i18n import gettext as _
from bot.analytics.types import ProductList
from bot.cache.redis import save_product_with_pipeline
from bot.keyboards.inline.category_kbd import product_detail, MainCallback
from bot.services.get_image import AikoClient
from bot.services.one_c import ONECClient


async def product_handler(query: types.CallbackQuery, callback_data: MainCallback):
    """
        Get products by Category Code 
    """
    product_code = callback_data.product_code
    artikuls = []
    # discount_price = None
    img_url = None
    extract_url = None

    api_client = ONECClient()
    async with api_client:
        post_data = {
            "detail": product_code,
            "admin": True
        }
        post_response = await api_client.fetch_data(post_data, model=ProductList)
    
    # _, products = await find_duplicate_codes(sub_category_list=post_response)
    async with AikoClient() as client:
        for product in post_response.goods:
            # success = False
            try:
                code = product.DetailSiteCode[5:] if "AIKO" in product.DetailSiteCode else product.DetailSiteCode    
                img_url = await client.fetch_image_url(code=code)
                # discount_price = await client.extract_prices(code=code)
                extract_url = await client.extract_href(code=code)
                success = True
            except AttributeError:
                success = False
            if success:
                break

    text = f"<b>{post_response.goods[0].name}</b>\n\n"
    for product in post_response.goods:
        #price = product.saledealerprices if product.saledealerprices != 0 else product.dealerprices
        artikuls.append({
            "name": product.DetailSiteCode,
            "quantity": 0,
            "price": product.exportprices,
            "detail": product.Detail,
            "max_qty": product.stock
        })
        
        text += _("Artikul: <b>{}</b>\n").format(product.DetailSiteCode)
        text += _("Xarakteristika: <b>{}</b>\n").format(product.Detail)
        text += _("Narxi: <b>{:,.0f}$</b>\n").format(product.exportprices).replace(",", " ")
        # if product.saleprices != 0:
        #     text += _("Chegirma narxi: <b>{:,.0f} so`m</b>\n").format(product.saleprices).replace(",", " ")
        # text += _("Diler narxi: <b>{:,.0f}$</b>\n").format(product.dealerprices).replace(",", " ")
        # if product.saledealerprices != 0:
        #     text += _("Diler chegirma narxi: <b>{:,.0f}$</b>\n").format(product.saledealerprices).replace(",", " ")
        text += _("Qoldi: <b>{}</b>\n\n").format(product.stock)

    text += f"https://aiko.uz{extract_url if extract_url else ''}"

    # Combine all data into a single JSON object
    user_data = {
        "post_response": post_response,
        "img_url": img_url,
        "extract_url": extract_url,
        "artikuls": artikuls,
        "text": text
    }

    await save_product_with_pipeline(user_id=query.from_user.id, data=user_data)

    await query.message.edit_text(
        text=text,
        reply_markup=product_detail(
            category_code=callback_data.category_code,
            brand=callback_data.brand,
            artikuls=artikuls,
        ),
        link_preview_options=types.LinkPreviewOptions(
            url=f"https://aiko.uz{img_url.strip()}" if img_url else None,
        )
    )
    await query.answer()