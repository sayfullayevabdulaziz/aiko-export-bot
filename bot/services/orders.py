from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import select, update

from bot.database.models import Order, OrderItem
from bot.database.models.orders import OrderStatusEnum

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def add_order(
    session: AsyncSession,
    user_id: int,
    cart_items: list,
) -> None:
    """Add Order."""
    order = Order(
            user_id=user_id,
        )

    session.add(order)
    await session.commit()
    await session.refresh(order)
    
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            artikul_id=item.artikul_id,
            quantity=item.quantity,
            price=item.price,
            name=item.name,
            detail=item.detail,
        )

        session.add(order_item)
        await session.commit()
        await session.refresh(order_item)

    return order


async def update_order_status(
    session: AsyncSession,
    order_id: str,
    accepted_user_id: int,
) -> None:
    """Update order status."""
    await session.execute(
        update(Order)
        .where(Order.id == order_id)
        .values(who_accept=accepted_user_id, status=OrderStatusEnum.IN_PROGRESS)
    )
    await session.commit()


async def get_user_id_by_order_id(
    session: AsyncSession,
    order_id: str,
) -> int:
    """Get user id by order id."""
    query = select(Order.user_id).where(Order.id == order_id)

    result = await session.execute(query)

    return result.scalar_one()