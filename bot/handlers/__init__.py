from aiogram import Router


def get_handlers_router() -> Router:
    from . import (
        start, 
        about, 
        back, 
        change_language, 
        category, 
        inline_finder, 
        cart, 
        cart_inline, 
        accept_user,
        order,
        export_users,
        catalogue,
        price_list,
    )

    router = Router()
    router.include_router(start.router)
    router.include_router(about.router)
    router.include_router(back.router)
    router.include_router(change_language.router)
    router.include_router(category.router)
    router.include_router(inline_finder.router)
    router.include_router(cart.router)
    router.include_router(cart_inline.router)
    router.include_router(accept_user.router)
    router.include_router(order.router)
    router.include_router(export_users.router)
    router.include_router(catalogue.router)
    router.include_router(price_list.router)
    # router.include_router(sub_category.router)

    return router
