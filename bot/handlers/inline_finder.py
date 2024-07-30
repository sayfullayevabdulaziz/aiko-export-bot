from aiogram import Router, F
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
    LinkPreviewOptions,
)
from aiogram.utils.i18n import gettext as _

from bot.analytics.types import ProductList, SubCategoryList
from bot.cache.redis import save_product_with_pipeline
from bot.keyboards.inline.back import back_keyboard
from bot.keyboards.inline.inline_query_kbd import product_detail_for_inline
from bot.keyboards.inline.menu import main_keyboard
from bot.services.get_image import AikoClient
from bot.services.one_c import ONECClient

router = Router(name="inline_finder")
# photo_id = "AgACAgIAAxkBAAICQWZ6WDp79MKmZdWlG7Sg3CPOirqjAAKO2DEbrpXZSyoIvVyqV465AQADAgADeAADNQQ"

@router.inline_query(F.query.len() < 3)
async def get_demo_inline(inline_query: InlineQuery):
    result = [InlineQueryResultArticle(
        id="demo_photo", 
        # thumbnail_url="https://api.telegram.org/file/bot6878127996:AAEU5NgtEXGr375aBP1p13hYGzTmYVbIrTs/photos/file_0.jpg",
        thumbnail_url="https://aiko.uz/wa-data/public/site/themes/insales_premium/img/logo-f.png?v1680511550?v1.2.0.190",
        thumbnail_width=50, thumbnail_height=50,
        title=_("Mahsulot nomini kiriting"),
        description=_("Minimal qiymat 3 ta belgi"),
        input_message_content=InputTextMessageContent(message_text="none",),
        )
    ]
    
    await inline_query.answer(result)


@router.inline_query(F.query.len() >= 3)
async def find_product(inline_query: InlineQuery):
    
    api_client = ONECClient()
    async with api_client:
        post_data = {
            "find": inline_query.query,
        }
        post_response = await api_client.fetch_data(brand="wood", data=post_data, model=SubCategoryList)
        if not post_response.goods:
            post_response = await api_client.fetch_data(brand="rattan", data=post_data, model=SubCategoryList)
    
    results = []
    if not post_response.goods:
        results.append(InlineQueryResultArticle(
            id="not_find", 
            # thumbnail_url="https://api.telegram.org/file/bot6878127996:AAEU5NgtEXGr375aBP1p13hYGzTmYVbIrTs/photos/file_0.jpg",
            thumbnail_url="https://aiko.uz/wa-data/public/site/themes/insales_premium/img/logo-f.png?v1680511550?v1.2.0.190",
            thumbnail_width=50, thumbnail_height=50,
            title=_("Mahsulot topilmadi"),
            input_message_content=InputTextMessageContent(message_text="none",),
        ))
        await inline_query.answer(
            results, is_personal=True, cache_time=60,
        )
        
    else:
        for product in post_response.goods:
            # В итоговый массив запихиваем каждую запись
            results.append(InlineQueryResultArticle(
                id=product.code,  # ссылки у нас уникальные, потому проблем не будет
                title=product.name,
                description=_("Qoldi: {}").format(product.stock),
                input_message_content=InputTextMessageContent(
                    message_text=product.code
                ),
            ))
        # Важно указать is_personal=True!
        await inline_query.answer(
            results, is_personal=True, cache_time=1,
        )

@router.message(F.via_bot, F.text == "none")
async def not_chosen(message: Message):
    await message.delete()
    await message.answer(_("Asosiy menu"), reply_markup=main_keyboard(),)


@router.message(F.via_bot)
async def chosen(message: Message):
    await message.delete()
    product_code = message.text
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
        # price = product.saledealerprices if product.saledealerprices != 0 else product.dealerprices
        artikuls.append({"name": product.DetailSiteCode, "quantity": 0, "price": product.exportprices, "detail": product.Detail, "max_qty": product.stock})
        
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

    user_data = {
        "post_response": post_response,
        "code": code,
        "img_url": img_url,
        "extract_url": extract_url,
        "artikuls": artikuls,
        "text": text
    }

    await save_product_with_pipeline(user_id=message.from_user.id, data=user_data)

    await message.answer(
        text=text,
        reply_markup=product_detail_for_inline(artikuls=artikuls),
        link_preview_options=LinkPreviewOptions(
            url=f"https://aiko.uz{img_url.strip()}" if img_url else None,
        ),
    )
