from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import select, delete, update, and_

from bot.analytics.types import ProductList
from bot.cache.redis import build_key, cached, clear_cache
from bot.database.models import CartItem
from bot.services.one_c import ONECClient

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def upsert_cart_item(
    session: AsyncSession,
    user_id: int,
    cart_items: dict,
    product_name: str,
) -> None:
    """Add/Update cart item."""
    
    for artikul, quantity_and_price in cart_items.items():
        # quantity, price = map(int, quantity_and_price.split(':'))
        
        if await exists_artikul(session, user_id, artikul):
            await update_artikul_quantity(session, user_id, artikul, quantity_and_price["quantity"], quantity_and_price["price"])
        else:
            api_client = ONECClient()
            async with api_client:
                post_data = {
                    "articul_id": artikul,
                    "admin": "true"
                }
                post_response = await api_client.fetch_data(brand="wood", data=post_data, model=ProductList)
                brand = "wood"
                if not post_response.goods:
                    post_response = await api_client.fetch_data(brand="rattan", data=post_data, model=ProductList)
                    brand = "rattan"
            
            cart_item = CartItem(
                user_id=user_id,
                artikul_id=artikul,
                quantity=quantity_and_price["quantity"],
                price=quantity_and_price["price"],
                name=product_name,
                detail=post_response.goods[0].Detail,
                brand=brand,
            )

            session.add(cart_item)
            await session.commit()


@cached(key_builder=lambda session, user_id: build_key(user_id))
async def get_cart_items(session: AsyncSession, user_id: int) -> str:
    query = select(CartItem).where(CartItem.user_id==user_id)

    result = await session.execute(query)

    cart_items = result.scalars().all()
    return cart_items


async def clear_cart(session: AsyncSession, user_id: int) -> None:
    query = delete(CartItem).where(CartItem.user_id==user_id)

    await session.execute(query)
    await session.commit()
    await clear_cache(get_cart_items, user_id)


async def delete_from_cart(session: AsyncSession, user_id: int, artikul: str) -> None:
    stmt = delete(CartItem).where(
        and_(CartItem.user_id == user_id, CartItem.artikul_id == artikul)
        )

    await session.execute(stmt)
    await session.commit()
    await clear_cache(get_cart_items, user_id)


async def exists_artikul(session: AsyncSession, user_id: int, artikul: str) -> bool:
    query = select(CartItem).where(CartItem.user_id==user_id, CartItem.artikul_id==artikul)

    result = await session.execute(query)

    return bool(result.scalars().first())


async def update_artikul_quantity(session: AsyncSession, user_id: int, artikul: str, quantity: int, price: int) -> None:
    stmt = update(CartItem).where(
        and_(CartItem.user_id == user_id, CartItem.artikul_id == artikul)
        ).values(quantity=quantity, price=price)

    await session.execute(stmt)
    await session.commit()
