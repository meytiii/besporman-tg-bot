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
    stmt = (
        select(Order)
        .options(selectinload(Order.user))
        .where(Order.public_order_number == public_order_number)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_order_by_id(session: AsyncSession, order_id: int) -> Optional[Order]:
    stmt = (
        select(Order)
        .options(selectinload(Order.user))
        .where(Order.id == order_id)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_user_orders(session: AsyncSession, user_id: int) -> List[Order]:
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
    order = await get_order_by_id(session, order_id)
    if not order:
        return None

    order.status = new_status
    order.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(order)
    return order

async def get_orders_by_status(session: AsyncSession, status: str) -> List[Order]:
    stmt = (
        select(Order)
        .options(selectinload(Order.user))
        .where(Order.status == status)
        .order_by(Order.created_at.desc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())

async def get_active_orders(session: AsyncSession) -> List[Order]:
    stmt = (
        select(Order)
        .options(selectinload(Order.user))
        .where(Order.status.not_in([OrderStatus.CLOSED, OrderStatus.REJECTED]))
        .order_by(Order.created_at.desc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())
