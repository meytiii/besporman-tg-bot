"""Main entrypoint for Bespor Man Telegram bot.

Runs either Long Polling or Webhook server depending on configuration.
"""

import asyncio
import logging
import sys
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from besporman_tg_bot.bot import create_bot, create_dispatcher
from besporman_tg_bot.core.config import settings
from besporman_tg_bot.db.base import async_session_factory, init_db
from besporman_tg_bot.db.seed import seed_initial_data

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("besporman_tg_bot")


async def on_startup(bot) -> None:
    """Pre-flight tasks: DB initialization, schema validation, and seeding."""
    logger.info("Initializing database...")
    await init_db()

    logger.info("Checking initial seed data...")
    async with async_session_factory() as session:
        await seed_initial_data(session)

    logger.info("Bespor Man bot initialized successfully.")


async def run_polling() -> None:
    """Run bot via Long Polling mode."""
    bot = create_bot()
    dp = create_dispatcher()

    await on_startup(bot)

    # Drop any pending updates accumulated while offline
    logger.info("Dropping pending updates and starting polling...")
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


def run_webhook() -> None:
    """Run bot via Webhook server mode."""
    bot = create_bot()
    dp = create_dispatcher()

    app = web.Application()

    async def on_app_startup(app: web.Application) -> None:
        await on_startup(bot)
        full_webhook_url = f"{settings.WEBHOOK_URL.rstrip('/')}{settings.WEBHOOK_PATH}"
        logger.info("Setting webhook to: %s", full_webhook_url)
        await bot.set_webhook(
            url=full_webhook_url,
            drop_pending_updates=True,
        )

    async def on_app_shutdown(app: web.Application) -> None:
        logger.info("Removing webhook...")
        await bot.delete_webhook()
        await bot.session.close()

    app.on_startup.append(on_app_startup)
    app.on_shutdown.append(on_app_shutdown)

    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_handler.register(app, path=settings.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    logger.info(
        "Starting webhook server on %s:%d ...",
        settings.WEBAPP_HOST,
        settings.WEBAPP_PORT,
    )
    web.run_app(
        app,
        host=settings.WEBAPP_HOST,
        port=settings.WEBAPP_PORT,
    )


def main() -> None:
    """CLI entrypoint."""
    if settings.WEBHOOK_MODE:
        run_webhook()
    else:
        asyncio.run(run_polling())


if __name__ == "__main__":
    main()
