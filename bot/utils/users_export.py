from __future__ import annotations
import csv
import io
import pandas as pd
from datetime import datetime, timezone

from aiogram.types import BufferedInputFile

from bot.database.models import UserModel


async def convert_users_to_csv(users: list[UserModel]) -> BufferedInputFile:
    """Export all users in csv file."""
    columns = UserModel.__table__.columns
    data = [[getattr(user, column.name) for column in columns] for user in users]

    s = io.StringIO()
    csv.writer(s).writerow(columns)
    csv.writer(s).writerows(data)
    s.seek(0)

    return BufferedInputFile(
        file=s.getvalue().encode("utf-8"),
        filename=f"users_{datetime.now(timezone.utc).strftime('%Y.%m.%d_%H.%M')}.csv",
    )

async def pydantic_model_to_df(products):
    data = [product.model_dump(exclude=["code", "DetailCode"]) for product in products]
    df = pd.DataFrame(data)
    return df


async def df_to_excel_binary(df):

    header_value = {
        "name": "Номенклатура", 
        "DetailSiteCode": "Артикул", 
        "Detail": "Характеристика",
        "stock": "Остаток", 
        "prices": "Цена", 
        "saleprices": "Цена со скидкой",
        "dealerprices": "Дилерская цена",
        "saledealerprices": "Дилерская цена со скидкой",
    }

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, header_value[value], header_format)
    buffer.seek(0)
    return buffer