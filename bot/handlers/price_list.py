from datetime import datetime, timezone

from aiogram import types, Router, F
from aiogram.utils.i18n import gettext as _

from bot.analytics.types import ProductList
from bot.keyboards.inline.menu import main_keyboard
from bot.services.one_c import ONECClient
from bot.utils.users_export import df_to_excel_binary, pydantic_model_to_df

router = Router(name="price-list")

@router.callback_query(F.data.startswith("price_list:"))
async def price_list_handler(query: types.CallbackQuery) -> None:
    """Return main menu."""
    await query.answer()

    brand = query.data.split(":")[1]

    api_client = ONECClient()
    async with api_client:
        post_data = {
            "all": True,
            "admin": True,
        }
        post_response = await api_client.fetch_data(brand=brand, data=post_data, model=ProductList)

    # Convert to DataFrame
    df = await pydantic_model_to_df(post_response.goods)

    # Save to Excel in binary mode
    excel_buffer = await df_to_excel_binary(df)

    file = types.BufferedInputFile(excel_buffer.getvalue(), filename=f"{brand}_{datetime.now().strftime('%d-%m-%Y')}.xlsx")

    await query.message.answer_document(file)