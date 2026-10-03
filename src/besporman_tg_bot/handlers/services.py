"""Handlers for team service categories (زمینه های کاری)."""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from besporman_tg_bot.core import texts
from besporman_tg_bot.keyboards.user_kb import get_services_keyboard

router = Router(name="services")


@router.message(Command("services"))
@router.message(F.text == texts.BTN_SERVICES)
async def handle_services(message: Message) -> None:
    """Display the team work areas and capabilities."""
    await message.answer(
        text=texts.SERVICES_TEXT,
        reply_markup=get_services_keyboard(),
    )
