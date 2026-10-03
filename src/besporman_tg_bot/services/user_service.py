"""User service for managing bot users."""

from datetime import datetime
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from besporman_tg_bot.db.models import User


async def get_or_create_user(
    session: AsyncSession,
    telegram_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
) -> User:
    """Fetch existing user or create a new one."""
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        # Update user profile if changed
        updated = False
        if user.username != username:
            user.username = username
            updated = True
        if user.first_name != first_name:
            user.first_name = first_name
            updated = True
        if updated:
            user.updated_at = datetime.utcnow()
            await session.commit()
            await session.refresh(user)
        return user

    user = User(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> Optional[User]:
    """Retrieve a user by their Telegram numeric ID."""
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
