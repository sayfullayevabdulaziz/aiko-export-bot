from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.utils.i18n.core import I18n
from aiogram.client.default import DefaultBotProperties
# from redis.asyncio import ConnectionPool, Redis
import redis.asyncio as aioredis

from bot.core.config import I18N_DOMAIN, LOCALES_DIR, settings

# app = web.Application()

token = settings.BOT_TOKEN

bot = Bot(token=token, default=DefaultBotProperties(
                                        parse_mode=ParseMode.HTML, 
                                        link_preview_is_disabled=False, 
                                        protect_content=True
                                    )
)

redis_client = aioredis.from_url(
    f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    max_connections=10,
)

storage = RedisStorage(
    redis=redis_client,
    key_builder=DefaultKeyBuilder(with_bot_id=True),
)

dp = Dispatcher(storage=storage)

i18n: I18n = I18n(path=LOCALES_DIR, default_locale="en", domain=I18N_DOMAIN)

DEBUG = settings.DEBUG
