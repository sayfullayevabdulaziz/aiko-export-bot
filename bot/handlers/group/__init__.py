from aiogram import Router


def get_group_handlers_router() -> Router:
    from . import (
        get_id_handler,
        order_accept,
    )

    router = Router()
    router.include_router(get_id_handler.group_router)
    router.include_router(order_accept.router)
    
    return router
