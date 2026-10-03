"""Admin dashboard and management panel."""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from besporman_tg_bot.core import texts
from besporman_tg_bot.db.models import AdminAuditLog, Order, OrderStatus, User
from besporman_tg_bot.keyboards.admin_kb import get_admin_dashboard_keyboard
from besporman_tg_bot.middlewares.admin_filter import IsAdminFilter
from besporman_tg_bot.services.audit_service import get_recent_audit_logs
from besporman_tg_bot.services.order_service import get_active_orders, get_orders_by_status

router = Router(name="admin_panel")
router.message.filter(IsAdminFilter())
router.callback_query.filter(IsAdminFilter())


@router.message(Command("admin"))
@router.message(Command("panel"))
async def handle_admin_dashboard(message: Message, session: AsyncSession) -> None:
    """Show admin panel dashboard."""
    # Count stats
    total_users = (await session.execute(select(func.count(User.id)))).scalar() or 0
    total_orders = (await session.execute(select(func.count(Order.id)))).scalar() or 0
    new_orders = (await session.execute(select(func.count(Order.id)).where(Order.status == OrderStatus.NEW))).scalar() or 0

    panel_text = (
        f"⚙️ <b>پنل مدیریت تیم بسپر من</b>\n\n"
        f"👥 کل کاربران: {total_users}\n"
        f"📦 کل سفارشات: {total_orders}\n"
        f"🚨 سفارشات جدید: {new_orders}\n\n"
        f"از منوی زیر بخش مورد نظر را انتخاب کنید:"
    )

    await message.answer(
        text=panel_text,
        reply_markup=get_admin_dashboard_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("adm_list:"))
async def handle_admin_order_list(callback: CallbackQuery, session: AsyncSession) -> None:
    """List orders by filter (NEW / ACTIVE)."""
    await callback.answer()
    category = callback.data.split(":")[1]

    if category == "NEW":
        orders = await get_orders_by_status(session, OrderStatus.NEW)
        title = "🚨 سفارش های جدید"
    else:
        orders = await get_active_orders(session)
        title = "📋 سفارش های فعال"

    if not orders:
        if callback.message:
            await callback.message.edit_text(
                text=f"{title}\n\nهیچ موردی یافت نشد.",
                reply_markup=get_admin_dashboard_keyboard(),
            )
        return

    buttons = []
    for ord_item in orders[:10]:
        status_label = texts.STATUS_LABELS.get(ord_item.status, ord_item.status)
        btn_text = f"#{ord_item.public_order_number} - {status_label} - {ord_item.user.first_name or 'کاربر'}"
        buttons.append([InlineKeyboardButton(text=btn_text, callback_data=f"adm_view_order:{ord_item.id}")])

    buttons.append([InlineKeyboardButton(text="🔙 بازگشت به داشبورد", callback_data="adm_dashboard")])

    if callback.message:
        await callback.message.edit_text(
            text=f"{title} ({len(orders)} مورد):",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        )


@router.callback_query(F.data == "adm_dashboard")
async def handle_return_dashboard(callback: CallbackQuery, session: AsyncSession) -> None:
    """Return to dashboard menu."""
    await callback.answer()
    total_users = (await session.execute(select(func.count(User.id)))).scalar() or 0
    total_orders = (await session.execute(select(func.count(Order.id)))).scalar() or 0
    new_orders = (await session.execute(select(func.count(Order.id)).where(Order.status == OrderStatus.NEW))).scalar() or 0

    panel_text = (
        f"⚙️ <b>پنل مدیریت تیم بسپر من</b>\n\n"
        f"👥 کل کاربران: {total_users}\n"
        f"📦 کل سفارشات: {total_orders}\n"
        f"🚨 سفارشات جدید: {new_orders}\n\n"
        f"از منوی زیر بخش مورد نظر را انتخاب کنید:"
    )

    if callback.message:
        await callback.message.edit_text(
            text=panel_text,
            reply_markup=get_admin_dashboard_keyboard(),
            parse_mode="HTML",
        )


@router.callback_query(F.data == "adm_stats")
async def handle_admin_stats(callback: CallbackQuery, session: AsyncSession) -> None:
    """Display comprehensive system statistics."""
    await callback.answer()
    total_users = (await session.execute(select(func.count(User.id)))).scalar() or 0
    total_orders = (await session.execute(select(func.count(Order.id)))).scalar() or 0

    # Count by status
    status_counts = {}
    for st_key in texts.STATUS_LABELS.keys():
        count = (await session.execute(select(func.count(Order.id)).where(Order.status == st_key))).scalar() or 0
        status_counts[st_key] = count

    lines = [
        f"📊 <b>آمار تفکیکی وضعیت سفارشات:</b>\n",
        f"👥 کل کاربران: {total_users}",
        f"📦 کل سفارشات: {total_orders}\n",
    ]
    for st_key, label in texts.STATUS_LABELS.items():
        lines.append(f"{label}: {status_counts.get(st_key, 0)}")

    back_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 بازگشت به داشبورد", callback_data="adm_dashboard")]]
    )

    if callback.message:
        await callback.message.edit_text(
            text="\n".join(lines),
            reply_markup=back_kb,
            parse_mode="HTML",
        )


@router.callback_query(F.data == "adm_audit_logs")
async def handle_admin_audit_logs(callback: CallbackQuery, session: AsyncSession) -> None:
    """Display recent admin audit logs."""
    await callback.answer()
    logs = await get_recent_audit_logs(session, limit=10)

    if not logs:
        text = "📜 لاگ های اخیر:\n\nهنوز فعالیتی ثبت نشده است."
    else:
        log_lines = ["📜 <b>آخرین فعالیت های مدیریتی:</b>\n"]
        for log in logs:
            time_str = log.created_at.strftime("%H:%M:%S")
            log_lines.append(
                f"• [{time_str}] ادمین `{log.admin_telegram_id}`:\n  {log.action} - {log.details or ''}"
            )
        text = "\n".join(log_lines)

    back_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 بازگشت به داشبورد", callback_data="adm_dashboard")]]
    )

    if callback.message:
        await callback.message.edit_text(
            text=text,
            reply_markup=back_kb,
            parse_mode="HTML",
        )
