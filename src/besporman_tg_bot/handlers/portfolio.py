"""Handlers for portfolio showcase and project details."""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from besporman_tg_bot.core import texts
from besporman_tg_bot.keyboards.user_kb import (
    get_back_inline_keyboard,
    get_portfolio_detail_keyboard,
    get_portfolio_list_keyboard,
)
from besporman_tg_bot.services.portfolio_service import (
    get_active_portfolios,
    get_portfolio_by_id,
)

router = Router(name="portfolio")


@router.message(Command("portfolio"))
@router.message(F.text == texts.BTN_PORTFOLIO)
async def handle_portfolio_menu(message: Message, session: AsyncSession) -> None:
    """Show list of active portfolio items."""
    items = await get_active_portfolios(session)
    if not items:
        await message.answer(
            text=texts.NO_PORTFOLIO_ITEMS,
            reply_markup=get_back_inline_keyboard(),
        )
        return

    await message.answer(
        text=texts.PORTFOLIO_INTRO,
        reply_markup=get_portfolio_list_keyboard(items),
    )


@router.callback_query(F.data == "port_list")
async def handle_portfolio_list_callback(callback: CallbackQuery, session: AsyncSession) -> None:
    """Return to portfolio list."""
    await callback.answer()
    items = await get_active_portfolios(session)
    if not items:
        if callback.message:
            await callback.message.edit_text(
                text=texts.NO_PORTFOLIO_ITEMS,
                reply_markup=get_back_inline_keyboard(),
            )
        return

    if callback.message:
        await callback.message.edit_text(
            text=texts.PORTFOLIO_INTRO,
            reply_markup=get_portfolio_list_keyboard(items),
        )


@router.callback_query(F.data.startswith("port_detail:"))
async def handle_portfolio_detail(callback: CallbackQuery, session: AsyncSession) -> None:
    """Display detailed view for a single portfolio project."""
    await callback.answer()
    project_id = int(callback.data.split(":")[1])
    project = await get_portfolio_by_id(session, project_id)

    if not project:
        if callback.message:
            await callback.message.answer("این نمونه کار پیدا نشد.")
        return

    # Calculate prev and next project IDs
    all_projects = await get_active_portfolios(session)
    project_ids = [p.id for p in all_projects]
    prev_id = None
    next_id = None
    if project_id in project_ids:
        idx = project_ids.index(project_id)
        if idx > 0:
            prev_id = project_ids[idx - 1]
        if idx < len(project_ids) - 1:
            next_id = project_ids[idx + 1]

    caption_text = (
        f"<b>{project.title}</b>\n\n"
        f"{project.description}\n\n"
        f"🛠 <b>تکنولوژی ها:</b> {project.technologies}"
    )

    detail_kb = get_portfolio_detail_keyboard(
        current_id=project.id,
        prev_id=prev_id,
        next_id=next_id,
    )

    if callback.message:
        await callback.message.edit_text(
            text=caption_text,
            reply_markup=detail_kb,
            parse_mode="HTML",
        )
