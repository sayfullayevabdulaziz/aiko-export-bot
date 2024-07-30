from __future__ import annotations
from typing import TYPE_CHECKING

from aiogram.types import BotCommand, BotCommandScopeDefault

if TYPE_CHECKING:
    from aiogram import Bot


async def set_default_commands(bot: Bot) -> None:
    await remove_default_commands(bot)

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запуск бота")
        ],
        scope=BotCommandScopeDefault(),
        )

    """ Commands for admins
    for admin_id in await admin_ids():
        await bot.set_my_commands(
            [
                BotCommand(command=command, description=description)
                for command, description in admins_commands[language_code].items()
            ],
            scope=BotCommandScopeChat(chat_id=admin_id),
        )
    """


async def remove_default_commands(bot: Bot) -> None:
    await bot.delete_my_commands(scope=BotCommandScopeDefault())
