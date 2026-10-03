"""Test suite for portfolio, testimonials, and audit services."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from besporman_tg_bot.services.audit_service import get_recent_audit_logs, log_admin_action
from besporman_tg_bot.services.portfolio_service import (
    add_portfolio_media,
    create_portfolio,
    get_active_portfolios,
    get_portfolio_by_id,
)
from besporman_tg_bot.services.testimonial_service import (
    create_testimonial,
    get_active_testimonials,
    get_random_testimonial,
)


@pytest.mark.asyncio
async def test_portfolio_service(async_session: AsyncSession):
    """Verify portfolio creation, media attachment, and active querying."""
    p1 = await create_portfolio(
        session=async_session,
        title="وبسایت فروشگاهی",
        description="توضیحات سایت",
        technologies="Python, React",
        sort_order=1,
    )
    p2 = await create_portfolio(
        session=async_session,
        title="اپلیکیشن ویندوز",
        description="توضیحات ویندوز",
        technologies="C#, WPF",
        sort_order=2,
        is_active=False,  # Inactive
    )

    await add_portfolio_media(
        session=async_session,
        portfolio_id=p1.id,
        file_id="photo_123",
        caption="نمای صفحه اصلی",
    )

    active_items = await get_active_portfolios(async_session)
    assert len(active_items) == 1
    assert active_items[0].id == p1.id
    assert len(active_items[0].media) == 1
    assert active_items[0].media[0].file_id == "photo_123"

    fetched = await get_portfolio_by_id(async_session, p1.id)
    assert fetched is not None
    assert fetched.title == "وبسایت فروشگاهی"


@pytest.mark.asyncio
async def test_testimonial_service(async_session: AsyncSession):
    """Verify customer testimonial creation and random selection."""
    t1 = await create_testimonial(async_session, file_id="testim_1", caption="کارشون عالی بود", sort_order=1)
    t2 = await create_testimonial(async_session, file_id="testim_2", caption="خیلی سریع تحویل دادن", sort_order=2)

    active = await get_active_testimonials(async_session)
    assert len(active) == 2

    # Test random selection
    chosen = await get_random_testimonial(async_session)
    assert chosen is not None
    assert chosen.id in [t1.id, t2.id]

    # Test exclude logic
    another = await get_random_testimonial(async_session, exclude_id=t1.id)
    assert another is not None
    assert another.id == t2.id


@pytest.mark.asyncio
async def test_audit_log_service(async_session: AsyncSession):
    """Verify administrative audit logging."""
    await log_admin_action(
        session=async_session,
        admin_telegram_id=347382968,
        action="ORDER_ACCEPTED",
        entity_type="ORDER",
        entity_id=1001,
        details="Order accepted after negotiation",
    )

    logs = await get_recent_audit_logs(async_session)
    assert len(logs) == 1
    assert logs[0].admin_telegram_id == 347382968
    assert logs[0].action == "ORDER_ACCEPTED"
