"""Common handlers for /start, /cancel, and navigation."""

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from besporman_tg_bot.core import texts
from besporman_tg_bot.keyboards.user_kb import get_main_menu_keyboard

router = Router(name="common")


@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext) -> None:
    """Handle /start command by sending friendly welcome message and main menu."""
    await state.clear()
    await message.answer(
        text=texts.START_WELCOME,
        reply_markup=get_main_menu_keyboard(),
    )


@router.message(Command("cancel"))
@router.message(F.text == texts.BTN_CANCEL)
async def handle_cancel(message: Message, state: FSMContext) -> None:
    """Universal cancel handler."""
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    await message.answer(
        text=texts.ACTION_CANCELLED,
        reply_markup=get_main_menu_keyboard(),
    )


@router.callback_query(F.data == "nav_main_menu")
async def handle_nav_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    """Return to main menu via inline button."""
    await state.clear()
    await callback.answer()
    if callback.message:
        await callback.message.answer(
            text=texts.MAIN_MENU_PROMPT,
            reply_markup=get_main_menu_keyboard(),
        )
