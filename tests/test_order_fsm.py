"""Test suite for order creation, sequential numbers, statuses, and messages."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from besporman_tg_bot.db.models import OrderStatus, SenderType
from besporman_tg_bot.services.message_service import get_order_messages, save_message
from besporman_tg_bot.services.order_service import (
    create_order,
    get_active_orders,
    get_order_by_number,
    get_orders_by_status,
    update_order_status,
)
from besporman_tg_bot.services.user_service import get_or_create_user


@pytest.mark.asyncio
async def test_order_creation_and_sequential_numbering(async_session: AsyncSession):
    """Verify orders receive incremental public order numbers starting from 1001."""
    user1 = await get_or_create_user(async_session, telegram_id=5001, username="client1", first_name="Ali")
    user2 = await get_or_create_user(async_session, telegram_id=5002, username="client2", first_name="Reza")

    order1 = await create_order(async_session, user1.id, "پروژه وبسایت شخصی")
    assert order1.public_order_number == 1001
    assert order1.status == OrderStatus.NEW

    order2 = await create_order(async_session, user2.id, "پروژه نرم افزار حسابداری ویندوز")
    assert order2.public_order_number == 1002

    # Lookup by public number
    fetched = await get_order_by_number(async_session, 1001)
    assert fetched is not None
    assert fetched.user.telegram_id == 5001
    assert fetched.description == "پروژه وبسایت شخصی"


@pytest.mark.asyncio
async def test_order_status_transitions(async_session: AsyncSession):
    """Verify order statuses can be updated through the state system."""
    user = await get_or_create_user(async_session, telegram_id=6001, username="test_client")
    order = await create_order(async_session, user.id, "ربات اختصاصی تلگرام")
    assert order.status == OrderStatus.NEW

    # Update to UNDER_REVIEW
    updated = await update_order_status(async_session, order.id, OrderStatus.UNDER_REVIEW)
    assert updated is not None
    assert updated.status == OrderStatus.UNDER_REVIEW

    # Update to ACCEPTED
    accepted = await update_order_status(async_session, order.id, OrderStatus.ACCEPTED)
    assert accepted.status == OrderStatus.ACCEPTED

    # Filter by status
    accepted_orders = await get_orders_by_status(async_session, OrderStatus.ACCEPTED)
    assert len(accepted_orders) == 1
    assert accepted_orders[0].id == order.id

    # Close order and verify active orders filter
    await update_order_status(async_session, order.id, OrderStatus.CLOSED)
    active_orders = await get_active_orders(async_session)
    assert order.id not in [o.id for o in active_orders]


@pytest.mark.asyncio
async def test_order_message_persistence(async_session: AsyncSession):
    """Verify messages from client and admin persist and link correctly to order."""
    user = await get_or_create_user(async_session, telegram_id=7001, username="msg_client")
    order = await create_order(async_session, user.id, "سیستم CRM اختصاصی")

    # Client message
    await save_message(
        session=async_session,
        user_id=user.id,
        sender_type=SenderType.CLIENT,
        sender_id=7001,
        content="توضیحات اولیه پروژه",
        order_id=order.id,
    )

    # Admin message
    await save_message(
        session=async_session,
        user_id=user.id,
        sender_type=SenderType.ADMIN,
        sender_id=347382968,
        content="بودجه تقریبی چقدر است؟",
        order_id=order.id,
    )

    messages = await get_order_messages(async_session, order.id)
    assert len(messages) == 2
    assert messages[0].sender_type == SenderType.CLIENT
    assert messages[1].sender_type == SenderType.ADMIN
