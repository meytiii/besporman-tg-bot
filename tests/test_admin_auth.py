import pytest
from unittest.mock import MagicMock
from aiogram.types import User as TgUser, Message, CallbackQuery

from besporman_tg_bot.core.config import settings
from besporman_tg_bot.middlewares.admin_filter import IsAdminFilter

@pytest.mark.asyncio
async def test_admin_filter_authorized_ids():
    admin_filter = IsAdminFilter()

    for admin_id in [347382968, 106629087]:
        msg = MagicMock(spec=Message)
        msg.from_user = TgUser(id=admin_id, is_bot=False, first_name="Admin", username="admin_user")
        assert await admin_filter(msg) is True

        cb = MagicMock(spec=CallbackQuery)
        cb.from_user = TgUser(id=admin_id, is_bot=False, first_name="Admin", username="admin_user")
        assert await admin_filter(cb) is True

@pytest.mark.asyncio
async def test_admin_filter_unauthorized_ids():
    admin_filter = IsAdminFilter()

    unauthorized_ids = [12345678, 99999999, 11111111]

    for user_id in unauthorized_ids:
        msg = MagicMock(spec=Message)
        msg.from_user = TgUser(id=user_id, is_bot=False, first_name="Hacker", username="admin")
        assert await admin_filter(msg) is False

@pytest.mark.asyncio
async def test_admin_filter_none_user():
    admin_filter = IsAdminFilter()
    msg = MagicMock(spec=Message)
    msg.from_user = None
    assert await admin_filter(msg) is False
