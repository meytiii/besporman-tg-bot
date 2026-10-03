from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from besporman_tg_bot.core import texts
from besporman_tg_bot.core.config import settings
from besporman_tg_bot.db.models import SenderType, User
from besporman_tg_bot.keyboards.user_kb import get_cancel_keyboard, get_main_menu_keyboard
from besporman_tg_bot.services.message_service import save_message
from besporman_tg_bot.states.user_states import SupportStates
from besporman_tg_bot.utils.profanity_filter import is_profane

router = Router(name="support")

@router.message(Command("support"))
@router.message(F.text == texts.BTN_SUPPORT)
async def handle_support_start(message: Message, state: FSMContext) -> None:
    await state.set_state(SupportStates.waiting_for_message)
    await message.answer(
        text=texts.SUPPORT_INTRO,
        reply_markup=get_cancel_keyboard(),
    )

@router.message(SupportStates.waiting_for_message, F.text)
async def handle_support_message(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    db_user: User,
    bot: Bot,
) -> None:
    content = message.text.strip()

    if is_profane(content):
        await message.answer(texts.PROFANITY_BLOCKED)
        return

    await save_message(
        session=session,
        user_id=db_user.id,
        sender_type=SenderType.CLIENT,
        sender_id=message.from_user.id,
        content=content,
        order_id=None,
        telegram_message_id=message.message_id,
    )

    await state.clear()

    await message.answer(
        text=texts.SUPPORT_RECEIVED,
        reply_markup=get_main_menu_keyboard(),
    )

    client_name = message.from_user.full_name or "نامشخص"
    username_str = f"@{message.from_user.username}" if message.from_user.username else "ندارد"

    admin_text = (
        f"💬 پیام پشتیبانی جدید\n\n"
        f"👤 کاربر: {client_name} ({username_str})\n"
        f"🆔 شناسه کاربری: `{message.from_user.id}`\n\n"
        f"📝 متن پیام:\n"
        f"────────────────\n"
        f"{content}\n"
        f"────────────────"
    )

    admin_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 پاسخ به کاربر", callback_data=f"adm_support_reply:{message.from_user.id}")]
        ]
    )

    for admin_id in settings.ADMIN_IDS:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=admin_text,
                reply_markup=admin_kb,
                parse_mode="Markdown",
            )
        except Exception:
            pass
