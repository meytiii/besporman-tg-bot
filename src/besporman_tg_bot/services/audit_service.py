from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from besporman_tg_bot.db.models import AdminAuditLog

async def log_admin_action(
    session: AsyncSession,
    admin_telegram_id: int,
    action: str,
    entity_type: str,
    entity_id: Optional[int] = None,
    details: Optional[str] = None,
) -> AdminAuditLog:
    log_entry = AdminAuditLog(
        admin_telegram_id=admin_telegram_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details,
        created_at=datetime.utcnow(),
    )
    session.add(log_entry)
    await session.commit()
    await session.refresh(log_entry)
    return log_entry

async def get_recent_audit_logs(
    session: AsyncSession,
    limit: int = 50,
) -> List[AdminAuditLog]:
    stmt = (
        select(AdminAuditLog)
        .order_by(AdminAuditLog.created_at.desc())
        .limit(limit)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())
