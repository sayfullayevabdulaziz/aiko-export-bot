# ruff: noqa: TCH001, TCH003, A003, F821
from __future__ import annotations

from enum import Enum

from aiogram.utils.i18n import gettext as _
import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from bot.database.models.base import Base
from bot.utils.order_generate import generate_order_id


class OrderStatusEnum(Enum):
    WAITING_FOR_WORKER = 'Kutish'
    IN_PROGRESS = 'Jarayonda'
    DONE = 'Bajarildi'


class Order(Base):
    id: Mapped[str] = mapped_column(primary_key=True, unique=True, index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, nullable=False)
    who_accept: Mapped[int] = mapped_column(sa.BigInteger, nullable=True)
    status: Mapped[PgEnum] = mapped_column(PgEnum(OrderStatusEnum, name='order_status_enum', create_type=False), nullable=False, default=OrderStatusEnum.WAITING_FOR_WORKER)

    items: Mapped[list[OrderItem]] = relationship(cascade="all,delete")
    # product_code: Mapped[str] = mapped_column(nullable=True)


@event.listens_for(Order, "before_insert")
def order_id_before_insert_event(mapper, connect, target):
    if not target.id:
        target.id = generate_order_id()


class OrderItem(Base):
    order_id: Mapped[int] = mapped_column(sa.ForeignKey("order.id"), nullable=True)
    artikul_id: Mapped[str] = mapped_column(nullable=True)
    quantity: Mapped[int] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(default=0, type_=sa.DECIMAL(10, 2))
    name: Mapped[str]
    detail: Mapped[str]