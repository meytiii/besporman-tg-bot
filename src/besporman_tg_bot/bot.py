"""Bot initialization, middleware registration, and router aggregation."""

import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from besporman_tg_bot.core.config import settings
from besporman_tg_bot.handlers import (
    admin_bridge,
    admin_orders,
    admin_panel,
    common,
    order,
    portfolio,
    services,
    support,
    team,
    testimonials,
)
from besporman_tg_bot.middlewares.db_middleware import DbSessionMiddleware
from besporman_tg_bot.middlewares.throttling_middleware import ThrottlingMiddleware
from besporman_tg_bot.middlewares.user_middleware import UserMiddleware

logger = logging.getLogger(__name__)


def create_bot() -> Bot:
    """Create configured Bot instance."""
    return Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def create_dispatcher() -> Dispatcher:
    """Create Dispatcher, register middlewares and attach routers."""
    dp = Dispatcher(storage=MemoryStorage())

    # Middlewares
    dp.update.outer_middleware(DbSessionMiddleware())
    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(UserMiddleware())
    dp.message.middleware(ThrottlingMiddleware())

    # Routers
    dp.include_router(common.router)
    dp.include_router(services.router)
    dp.include_router(order.router)
    dp.include_router(portfolio.router)
    dp.include_router(testimonials.router)
    dp.include_router(team.router)
    dp.include_router(support.router)
    dp.include_router(admin_orders.router)
    dp.include_router(admin_bridge.router)
    dp.include_router(admin_panel.router)

    return dp
