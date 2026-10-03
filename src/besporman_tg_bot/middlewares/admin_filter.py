"""Administrator authorization filters and checks."""

from typing import Union
from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

from besporman_tg_bot.core.config import settings


class IsAdminFilter(Filter):
    """Filter that allows updates only from configured numeric Telegram Admin IDs."""

    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        user = event.from_user
        if not user:
            return False
        return user.id in settings.ADMIN_IDS
