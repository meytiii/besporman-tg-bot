"""Testimonial service for managing customer satisfaction showcases."""

from datetime import datetime
from typing import List, Optional
import random
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from besporman_tg_bot.db.models import Testimonial


async def get_active_testimonials(session: AsyncSession) -> List[Testimonial]:
    """Retrieve all active testimonials."""
    stmt = (
        select(Testimonial)
        .where(Testimonial.is_active.is_(True))
        .order_by(Testimonial.sort_order.asc(), Testimonial.id.asc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_random_testimonial(
    session: AsyncSession,
    exclude_id: Optional[int] = None,
) -> Optional[Testimonial]:
    """Retrieve a random active testimonial, preferring one different from exclude_id."""
    items = await get_active_testimonials(session)
    if not items:
        return None

    if len(items) > 1 and exclude_id is not None:
        candidates = [t for t in items if t.id != exclude_id]
        if candidates:
            return random.choice(candidates)

    return random.choice(items)


async def create_testimonial(
    session: AsyncSession,
    file_id: str,
    caption: Optional[str] = None,
    sort_order: int = 0,
    is_active: bool = True,
) -> Testimonial:
    """Create a new testimonial entry."""
    item = Testimonial(
        file_id=file_id.strip(),
        caption=caption.strip() if caption else None,
        sort_order=sort_order,
        is_active=is_active,
        created_at=datetime.utcnow(),
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item
