"""Message service for logging client and admin communications."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from besporman_tg_bot.db.models import Message


async def save_message(
    session: AsyncSession,
    user_id: int,
    sender_type: str,
    sender_id: int,
    content: str,
    order_id: Optional[int] = None,
    message_type: str = "TEXT",
    telegram_message_id: Optional[int] = None,
) -> Message:
    """Save an incoming or outgoing message to database history."""
    msg = Message(
        order_id=order_id,
        user_id=user_id,
        sender_type=sender_type,
        sender_id=sender_id,
        message_type=message_type,
        content=content.strip(),
        telegram_message_id=telegram_message_id,
        created_at=datetime.utcnow(),
    )
    session.add(msg)
    await session.commit()
    await session.refresh(msg)
    return msg


async def get_order_messages(session: AsyncSession, order_id: int) -> List[Message]:
    """Retrieve message history for an order."""
    stmt = (
        select(Message)
        .where(Message.order_id == order_id)
        .order_by(Message.created_at.asc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())
