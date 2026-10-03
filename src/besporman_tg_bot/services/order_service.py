"""Order service for creating and managing client orders."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from besporman_tg_bot.db.models import Order, OrderStatus, User


async def create_order(
    session: AsyncSession,
    user_id: int,
    description: str,
) -> Order:
    """Create a new client order with a unique sequential public order number."""
    # Compute next public order number starting from 1001
    stmt = select(func.max(Order.public_order_number))
    result = await session.execute(stmt)
    max_num = result.scalar()
    next_order_num = 1001 if max_num is None else max_num + 1

    order = Order(
        public_order_number=next_order_num,
        user_id=user_id,
        description=description.strip(),
        status=OrderStatus.NEW,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


async def get_order_by_number(session: AsyncSession, public_order_number: int) -> Optional[Order]:
    """Retrieve an order by its public order number, with user eagerly loaded."""
    stmt = (
        select(Order)
        .options(selectinload(Order.user))
        .where(Order.public_order_number == public_order_number)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_order_by_id(session: AsyncSession, order_id: int) -> Optional[Order]:
    """Retrieve an order by primary key ID, with user eagerly loaded."""
    stmt = (
        select(Order)
        .options(selectinload(Order.user))
        .where(Order.id == order_id)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_orders(session: AsyncSession, user_id: int) -> List[Order]:
    """Retrieve all orders submitted by a specific user."""
    stmt = (
        select(Order)
        .where(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def update_order_status(
    session: AsyncSession,
    order_id: int,
    new_status: str,
) -> Optional[Order]:
    """Update order status safely."""
    order = await get_order_by_id(session, order_id)
    if not order:
        return None

    order.status = new_status
    order.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(order)
    return order


async def get_orders_by_status(session: AsyncSession, status: str) -> List[Order]:
    """Retrieve orders by status."""
    stmt = (
        select(Order)
        .options(selectinload(Order.user))
        .where(Order.status == status)
        .order_by(Order.created_at.desc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_active_orders(session: AsyncSession) -> List[Order]:
    """Retrieve active non-closed orders."""
    stmt = (
        select(Order)
        .options(selectinload(Order.user))
        .where(Order.status.not_in([OrderStatus.CLOSED, OrderStatus.REJECTED]))
        .order_by(Order.created_at.desc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())
