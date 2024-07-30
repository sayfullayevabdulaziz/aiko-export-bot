from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import func, select, update

from bot.cache.redis import build_key, cached, clear_cache
from bot.database.models import UserModel
from bot.database.models.user import ManagerModel, ClientModel

if TYPE_CHECKING:
    from aiogram.types import User
    from sqlalchemy.ext.asyncio import AsyncSession


async def add_user(
    session: AsyncSession,
    user: User,
    language_code: str | None = None,
) -> None:
    """Add a new user to the database."""
    user_id: int = user.id
    first_name: str = user.first_name
    last_name: str | None = user.last_name
    username: str | None = user.username
    language_code: str | None = user.language_code if language_code is None else language_code
    is_premium: bool = user.is_premium or False

    new_user = UserModel(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        language_code=language_code,
        is_premium=is_premium,
    )

    session.add(new_user)
    await session.commit()
    await clear_cache(user_exists, user_id)


@cached(key_builder=lambda session, user_id: build_key(user_id))
async def user_exists(session: AsyncSession, user_id: int) -> bool:
    """Checks if the user is in the database."""
    query = select(UserModel.user_id).filter_by(user_id=user_id).limit(1)

    result = await session.execute(query)

    user = result.scalar_one_or_none()
    return bool(user)


@cached(key_builder=lambda session, user_id: build_key(user_id))
async def get_first_name(session: AsyncSession, user_id: int) -> str:
    query = select(UserModel.first_name).filter_by(user_id=user_id)

    result = await session.execute(query)

    first_name = result.scalar_one_or_none()
    return first_name or ""


@cached(key_builder=lambda session, user_id: build_key(user_id))
async def get_language_code(session: AsyncSession, user_id: int) -> str:
    query = select(UserModel.language_code).where(UserModel.user_id==user_id)

    result = await session.execute(query)

    language_code = result.scalar_one_or_none()
    return language_code or ""


async def set_language_code(
    session: AsyncSession,
    user_id: int,
    language_code: str,
) -> None:
    stmt = update(UserModel).where(UserModel.user_id == user_id).values(language_code=language_code)

    await session.execute(stmt)
    await session.commit()
    await clear_cache(get_language_code, user_id)


async def set_phone(
    session: AsyncSession,
    user_id: int,
    phone: str,
) -> None:
    stmt = update(UserModel).where(UserModel.user_id == user_id).values(phone=phone, is_block=True)

    await session.execute(stmt)
    await session.commit()


async def update_block(session: AsyncSession, user_id: int, is_block: bool):
    stmt = update(UserModel).where(UserModel.user_id == user_id).values(is_block=is_block)

    await session.execute(stmt)
    await session.commit()


@cached(key_builder=lambda session, user_id: build_key(user_id))
async def is_admin(session: AsyncSession, user_id: int) -> bool:
    query = select(UserModel.is_admin).filter_by(user_id=user_id)

    result = await session.execute(query)

    is_admin = result.scalar_one_or_none()
    return bool(is_admin)


@cached(key_builder=lambda session: build_key("admins"))
async def get_admins(session: AsyncSession) -> list[UserModel]:
    query = select(UserModel).where(UserModel.is_admin==True)

    result = await session.execute(query)

    admins = result.scalars().all()
    return admins


@cached(key_builder=lambda session, user_id: build_key(user_id))
async def is_block(session: AsyncSession, user_id: int) -> bool:
    query = select(UserModel.is_block).filter_by(user_id=user_id)

    result = await session.execute(query)

    is_block = result.scalar_one_or_none()
    return bool(is_block)


async def set_is_admin(session: AsyncSession, user_id: int, is_admin: bool) -> None:
    stmt = update(UserModel).where(UserModel.user_id == user_id).values(is_admin=is_admin)

    await session.execute(stmt)
    await session.commit()


@cached(key_builder=lambda session: build_key())
async def get_all_users(session: AsyncSession) -> list[UserModel]:
    query = select(UserModel)

    result = await session.execute(query)

    users = result.scalars()
    return list(users)


@cached(key_builder=lambda session: build_key())
async def get_user_count(session: AsyncSession) -> int:
    query = select(func.count()).select_from(UserModel)

    result = await session.execute(query)

    count = result.scalar_one_or_none() or 0
    return int(count)


async def get_user(
    session: AsyncSession,
    user_id: int,
) -> UserModel | None:
    query = select(UserModel).where(UserModel.user_id == user_id)

    result = await session.execute(query)

    user = result.scalar_one_or_none()
    return user


async def get_phone_number(
    session: AsyncSession,
    user_id: int,
) -> str:
    query = select(UserModel.phone).where(UserModel.user_id == user_id)

    result = await session.execute(query)

    phone = result.scalar_one()
    return phone


async def get_manager(
    session: AsyncSession,
    client_phone: int,
) -> ManagerModel | None:
    query = select(ManagerModel).join(ClientModel, ManagerModel.id == ClientModel.manager_id).where(ClientModel.phone == client_phone)

    result = await session.execute(query)

    user = result.scalar_one_or_none()
    return user