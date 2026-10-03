"""Anti-flood and rate limiting middleware."""

import time
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, User as TgUser

from besporman_tg_bot.core.config import settings
from besporman_tg_bot.core import texts


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.user_timestamps: Dict[int, list[float]] = {}
        self.user_warned_at: Dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        event_from_user: TgUser = data.get("event_from_user")
        if not event_from_user:
            return await handler(event, data)

        user_id = event_from_user.id
        # Admin bypass
        if user_id in settings.ADMIN_IDS:
            return await handler(event, data)

        now = time.monotonic()
        history = self.user_timestamps.setdefault(user_id, [])

        # Evict timestamps older than RATE_LIMIT_PERIOD
        cutoff = now - settings.RATE_LIMIT_PERIOD
        self.user_timestamps[user_id] = [t for t in history if t > cutoff]

        if len(self.user_timestamps[user_id]) >= settings.RATE_LIMIT_BURST:
            # Check if warned recently
            last_warned = self.user_warned_at.get(user_id, 0.0)
            if now - last_warned > settings.RATE_LIMIT_PERIOD:
                self.user_warned_at[user_id] = now
                if isinstance(event, Message):
                    await event.answer(texts.RATE_LIMIT_WARNING)
            return None

        self.user_timestamps[user_id].append(now)
        return await handler(event, data)
