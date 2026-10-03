"""Handlers for administrative order management and status transitions."""

from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from besporman_tg_bot.core import texts
from besporman_tg_bot.keyboards.admin_kb import (
    get_admin_order_actions_keyboard,
    get_admin_status_selection_keyboard,
)
from besporman_tg_bot.middlewares.admin_filter import IsAdminFilter
from besporman_tg_bot.services.audit_service import log_admin_action
from besporman_tg_bot.services.order_service import get_order_by_id, update_order_status

router = Router(name="admin_orders")
router.message.filter(IsAdminFilter())
router.callback_query.filter(IsAdminFilter())


@router.callback_query(F.data.startswith("adm_view_order:"))
async def handle_view_order(callback: CallbackQuery, session: AsyncSession) -> None:
    """Return to order view with actions."""
    await callback.answer()
    order_id = int(callback.data.split(":")[1])
    order = await get_order_by_id(session, order_id)
    if not order:
        if callback.message:
            await callback.message.answer("سفارش مورد نظر یافت نشد.")
        return

    status_label = texts.STATUS_LABELS.get(order.status, order.status)
    content = (
        f"📋 سفارش #{order.public_order_number}\n\n"
        f"وضعیت فعلی: {status_label}\n"
        f"👤 مشتری: {order.user.first_name} (@{order.user.username or 'ندارد'})\n\n"
        f"📝 توضیحات:\n{order.description}"
    )

    if callback.message:
        await callback.message.edit_text(
            text=content,
            reply_markup=get_admin_order_actions_keyboard(order.id),
        )


@router.callback_query(F.data.startswith("adm_status_menu:"))
async def handle_status_menu(callback: CallbackQuery) -> None:
    """Show status selection keyboard for order."""
    await callback.answer()
    order_id = int(callback.data.split(":")[1])
    if callback.message:
        await callback.message.edit_text(
            text=f"وضعیت جدید را برای سفارش انتخاب کنید:",
            reply_markup=get_admin_status_selection_keyboard(order_id),
        )


@router.callback_query(F.data.startswith("adm_set_status:") | F.data.startswith("adm_quick_status:"))
async def handle_set_status(callback: CallbackQuery, session: AsyncSession) -> None:
    """Update order status and write to audit log."""
    await callback.answer()
    parts = callback.data.split(":")
    order_id = int(parts[1])
    new_status = parts[2]

    order = await get_order_by_id(session, order_id)
    if not order:
        if callback.message:
            await callback.message.answer("سفارش مورد نظر یافت نشد.")
        return

    old_status = order.status
    if old_status == new_status:
        if callback.message:
            await callback.message.answer("سفارش در حال حاضر در همین وضعیت قرار دارد.")
        return

    await update_order_status(session, order_id, new_status)

    # Record in audit trail
    await log_admin_action(
        session=session,
        admin_telegram_id=callback.from_user.id,
        action="ORDER_STATUS_CHANGED",
        entity_type="ORDER",
        entity_id=order_id,
        details=f"Status changed from {old_status} to {new_status} for order #{order.public_order_number}",
    )

    status_label = texts.STATUS_LABELS.get(new_status, new_status)
    notice = f"وضعیت سفارش #{order.public_order_number} با موفقیت به «{status_label}» تغییر یافت. ✅"

    if callback.message:
        await callback.message.edit_text(
            text=f"{notice}\n\n"
                 f"👤 مشتری: {order.user.first_name} (@{order.user.username or 'ندارد'})\n"
                 f"📝 توضیحات:\n{order.description}",
            reply_markup=get_admin_order_actions_keyboard(order.id),
        )
