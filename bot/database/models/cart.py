# ruff: noqa: TCH001, TCH003, A003, F821
from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.models.base import Base


class CartItem(Base):
    user_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=True)
    artikul_id: Mapped[str] = mapped_column(nullable=True)
    quantity: Mapped[int] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(default=0, type_=sa.DECIMAL(10, 2))
    name: Mapped[str]
    detail: Mapped[str]
    brand: Mapped[str] = mapped_column(sa.String(6), nullable=True)
    # product_code: Mapped[str] = mapped_column(nullable=True)