"""User registration and synchronization middleware."""

from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TgUser
from sqlalchemy.ext.asyncio import AsyncSession

from besporman_tg_bot.services.user_service import get_or_create_user


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        event_from_user: TgUser = data.get("event_from_user")
        session: AsyncSession = data.get("session")

        if event_from_user and session:
            db_user = await get_or_create_user(
                session=session,
                telegram_id=event_from_user.id,
                username=event_from_user.username,
                first_name=event_from_user.first_name,
            )
            data["db_user"] = db_user

        return await handler(event, data)
