"""Portfolio service for retrieving and managing team portfolio projects."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from besporman_tg_bot.db.models import Portfolio, PortfolioMedia


async def get_active_portfolios(session: AsyncSession) -> List[Portfolio]:
    """Retrieve all active portfolio items ordered by sort_order."""
    stmt = (
        select(Portfolio)
        .options(selectinload(Portfolio.media))
        .where(Portfolio.is_active.is_(True))
        .order_by(Portfolio.sort_order.asc(), Portfolio.id.asc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_portfolio_by_id(session: AsyncSession, portfolio_id: int) -> Optional[Portfolio]:
    """Retrieve single portfolio project with media attached."""
    stmt = (
        select(Portfolio)
        .options(selectinload(Portfolio.media))
        .where(Portfolio.id == portfolio_id)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_portfolio(
    session: AsyncSession,
    title: str,
    description: str,
    technologies: str,
    sort_order: int = 0,
    is_active: bool = True,
) -> Portfolio:
    """Create a new portfolio entry."""
    item = Portfolio(
        title=title.strip(),
        description=description.strip(),
        technologies=technologies.strip(),
        sort_order=sort_order,
        is_active=is_active,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def add_portfolio_media(
    session: AsyncSession,
    portfolio_id: int,
    file_id: str,
    media_type: str = "PHOTO",
    caption: Optional[str] = None,
    sort_order: int = 0,
) -> PortfolioMedia:
    """Attach media (photo/document) to a portfolio project."""
    media = PortfolioMedia(
        portfolio_id=portfolio_id,
        file_id=file_id.strip(),
        media_type=media_type,
        caption=caption.strip() if caption else None,
        sort_order=sort_order,
        created_at=datetime.utcnow(),
    )
    session.add(media)
    await session.commit()
    await session.refresh(media)
    return media
