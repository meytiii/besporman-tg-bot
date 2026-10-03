from datetime import datetime
from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from besporman_tg_bot.core import texts
from besporman_tg_bot.core.config import settings
from besporman_tg_bot.db.models import SenderType, User
from besporman_tg_bot.keyboards.admin_kb import get_admin_order_actions_keyboard
from besporman_tg_bot.keyboards.user_kb import get_cancel_keyboard, get_main_menu_keyboard
from besporman_tg_bot.services.message_service import save_message
from besporman_tg_bot.services.order_service import create_order
from besporman_tg_bot.services.portfolio_service import get_portfolio_by_id
from besporman_tg_bot.states.user_states import OrderStates
from besporman_tg_bot.utils.profanity_filter import is_profane

router = Router(name="order")

@router.message(Command("order"))
@router.message(F.text == texts.BTN_ORDER)
async def handle_order_start(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderStates.waiting_for_description)
    await message.answer(
        text=texts.ORDER_INTRO,
        reply_markup=get_cancel_keyboard(),
    )

@router.callback_query(F.data == "order_start")
async def handle_order_start_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(OrderStates.waiting_for_description)
    if callback.message:
        await callback.message.answer(
            text=texts.ORDER_INTRO,
            reply_markup=get_cancel_keyboard(),
        )

@router.callback_query(F.data.startswith("order_similar:"))
async def handle_order_similar_callback(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    await callback.answer()
    project_id = int(callback.data.split(":")[1])
    project = await get_portfolio_by_id(session, project_id)

    prompt = texts.ORDER_SIMILAR_PROMPT
    if project:
        prompt = (
            f"می خوای یه پروژه شبیه «{project.title}» برات پیاده سازی کنیم؟ عالیه! 😎\n\n"
            "توضیحات و ویژگی های اختصاصی که مد نظر داری رو برام بنویس 👇"
        )

    await state.set_state(OrderStates.waiting_for_description)
    await state.update_data(similar_project_id=project_id)

    if callback.message:
        await callback.message.answer(
            text=prompt,
            reply_markup=get_cancel_keyboard(),
        )

@router.message(OrderStates.waiting_for_description, F.text)
async def handle_order_description(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    db_user: User,
    bot: Bot,
) -> None:
    description = message.text.strip()

    if is_profane(description):
        await message.answer(texts.PROFANITY_BLOCKED)
        return

    state_data = await state.get_data()
    similar_id = state_data.get("similar_project_id")
    if similar_id:
        project = await get_portfolio_by_id(session, similar_id)
        if project:
            description = f"[سفارش مشابه پروژه: {project.title}]\n\n{description}"

    order = await create_order(
        session=session,
        user_id=db_user.id,
        description=description,
    )

    await save_message(
        session=session,
        user_id=db_user.id,
        sender_type=SenderType.CLIENT,
        sender_id=message.from_user.id,
        content=description,
        order_id=order.id,
        telegram_message_id=message.message_id,
    )

    await state.clear()

    await message.answer(
        text=texts.ORDER_CREATED_CONFIRMATION.format(order_number=order.public_order_number),
        reply_markup=get_main_menu_keyboard(),
    )

    client_name = message.from_user.full_name or "نامشخص"
    username_str = f"@{message.from_user.username}" if message.from_user.username else "ندارد"
    created_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    admin_notification = (
        f"🚨 سفارش جدید #{order.public_order_number}\n\n"
        f"👤 مشتری: {client_name} ({username_str})\n"
        f"🆔 شناسه کاربری: `{message.from_user.id}`\n\n"
        f"📝 توضیحات پروژه:\n"
        f"────────────────\n"
        f"{description}\n"
        f"────────────────\n\n"
        f"⏰ زمان ثبت: {created_time}"
    )

    for admin_id in settings.ADMIN_IDS:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=admin_notification,
                reply_markup=get_admin_order_actions_keyboard(order.id),
                parse_mode="Markdown",
            )
        except Exception:
            pass
