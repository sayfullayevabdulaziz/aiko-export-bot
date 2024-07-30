from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.users import is_block

class IsBlockedMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        session: AsyncSession = data["session"]
        user = event.from_user


        if not await is_block(session, user.id):
            return await handler(event, data)
        # print("After handler")
        return None