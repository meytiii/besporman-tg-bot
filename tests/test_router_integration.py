"""Integration test suite for aiogram handlers using mock events."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message, User as TgUser, Chat

from besporman_tg_bot.core import texts
from besporman_tg_bot.db.models import OrderStatus
from besporman_tg_bot.handlers.common import handle_start, handle_cancel
from besporman_tg_bot.handlers.order import handle_order_start, handle_order_description
from besporman_tg_bot.handlers.support import handle_support_start, handle_support_message
from besporman_tg_bot.services.order_service import get_orders_by_status
from besporman_tg_bot.services.user_service import get_or_create_user
from besporman_tg_bot.states.user_states import OrderStates, SupportStates


@pytest.fixture
def fsm_storage():
    return MemoryStorage()


def make_mock_message(user_id: int, text: str, message_id: int = 100):
    msg = MagicMock(spec=Message)
    msg.message_id = message_id
    msg.text = text
    msg.from_user = TgUser(id=user_id, is_bot=False, first_name="TestUser", username="testuser")
    msg.chat = Chat(id=user_id, type="private")
    msg.answer = AsyncMock()
    return msg


@pytest.mark.asyncio
async def test_start_and_cancel_handlers(fsm_storage):
    """Verify /start and cancel messages reset state and return main menu."""
    storage_key = StorageKey(bot_id=1, chat_id=123, user_id=123)
    fsm_ctx = FSMContext(storage=fsm_storage, key=storage_key)
    await fsm_ctx.set_state(OrderStates.waiting_for_description)

    msg = make_mock_message(123, "/start")
    await handle_start(msg, fsm_ctx)
    assert await fsm_ctx.get_state() is None
    msg.answer.assert_called_once()
    assert msg.answer.call_args[1]["text"] == texts.START_WELCOME

    # Test Cancel
    await fsm_ctx.set_state(SupportStates.waiting_for_message)
    cancel_msg = make_mock_message(123, texts.BTN_CANCEL)
    await handle_cancel(cancel_msg, fsm_ctx)
    assert await fsm_ctx.get_state() is None
    assert cancel_msg.answer.call_args[1]["text"] == texts.ACTION_CANCELLED


@pytest.mark.asyncio
async def test_order_submission_flow(async_session, fsm_storage):
    """Verify order submission flow from start to description intake and admin alert."""
    storage_key = StorageKey(bot_id=1, chat_id=456, user_id=456)
    fsm_ctx = FSMContext(storage=fsm_storage, key=storage_key)

    # 1. User starts order
    start_msg = make_mock_message(456, texts.BTN_ORDER)
    await handle_order_start(start_msg, fsm_ctx)
    assert await fsm_ctx.get_state() == OrderStates.waiting_for_description.state

    # 2. User provides project description
    db_user = await get_or_create_user(async_session, telegram_id=456, username="orderer", first_name="Client")
    desc_msg = make_mock_message(456, "یک وبسایت شرکتی با بخش بلاگ و نمونه کارها می خواهیم.")

    mock_bot = MagicMock()
    mock_bot.send_message = AsyncMock()

    await handle_order_description(
        message=desc_msg,
        state=fsm_ctx,
        session=async_session,
        db_user=db_user,
        bot=mock_bot,
    )

    # FSM cleared
    assert await fsm_ctx.get_state() is None

    # Confirmation sent to client
    desc_msg.answer.assert_called_once()
    assert "1001" in desc_msg.answer.call_args[1]["text"]

    # Verify order in DB
    orders = await get_orders_by_status(async_session, OrderStatus.NEW)
    assert len(orders) == 1
    assert orders[0].public_order_number == 1001

    # Verify admins received notification
    assert mock_bot.send_message.call_count == 2  # Notified both admins (347382968 and 106629087)


@pytest.mark.asyncio
async def test_support_submission_flow(async_session, fsm_storage):
    """Verify support inquiry intake and admin forwarding."""
    storage_key = StorageKey(bot_id=1, chat_id=789, user_id=789)
    fsm_ctx = FSMContext(storage=fsm_storage, key=storage_key)

    # 1. User starts support
    start_msg = make_mock_message(789, texts.BTN_SUPPORT)
    await handle_support_start(start_msg, fsm_ctx)
    assert await fsm_ctx.get_state() == SupportStates.waiting_for_message.state

    # 2. User sends support query
    db_user = await get_or_create_user(async_session, telegram_id=789, username="supporter", first_name="User")
    supp_msg = make_mock_message(789, "سلام، آیا برای پروژه های قدیمی هم پشتیبانی ارائه می دهید؟")

    mock_bot = MagicMock()
    mock_bot.send_message = AsyncMock()

    await handle_support_message(
        message=supp_msg,
        state=fsm_ctx,
        session=async_session,
        db_user=db_user,
        bot=mock_bot,
    )

    assert await fsm_ctx.get_state() is None
    supp_msg.answer.assert_called_once()
    assert supp_msg.answer.call_args[1]["text"] == texts.SUPPORT_RECEIVED
    assert mock_bot.send_message.call_count == 2
