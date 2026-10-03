from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from besporman_tg_bot.core import texts
from besporman_tg_bot.core.config import settings
from besporman_tg_bot.db.models import SenderType
from besporman_tg_bot.keyboards.admin_kb import (
    get_admin_cancel_keyboard,
    get_admin_order_actions_keyboard,
)
from besporman_tg_bot.middlewares.admin_filter import IsAdminFilter
from besporman_tg_bot.services.audit_service import log_admin_action
from besporman_tg_bot.services.message_service import save_message
from besporman_tg_bot.services.order_service import get_order_by_id
from besporman_tg_bot.services.user_service import get_user_by_telegram_id
from besporman_tg_bot.states.user_states import AdminBridgeStates, ClientBridgeStates

router = Router(name="admin_bridge")

@router.callback_query(IsAdminFilter(), F.data.startswith("adm_reply:"))
async def handle_admin_reply_click(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    order_id = int(callback.data.split(":")[1])
    await state.set_state(AdminBridgeStates.waiting_for_reply_content)
    await state.update_data(bridge_order_id=order_id, bridge_type="REPLY")

    if callback.message:
        await callback.message.answer(
            text=texts.ADMIN_PROMPT_REPLY,
            reply_markup=get_admin_cancel_keyboard(),
        )

@router.callback_query(IsAdminFilter(), F.data.startswith("adm_ask:"))
async def handle_admin_ask_click(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    order_id = int(callback.data.split(":")[1])
    await state.set_state(AdminBridgeStates.waiting_for_info_question)
    await state.update_data(bridge_order_id=order_id, bridge_type="ASK_INFO")

    if callback.message:
        await callback.message.answer(
            text=texts.ADMIN_PROMPT_REQUEST_INFO,
            reply_markup=get_admin_cancel_keyboard(),
        )

@router.callback_query(IsAdminFilter(), F.data == "adm_cancel")
async def handle_admin_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer("عملیات لغو شد.")
    if callback.message:
        await callback.message.delete()

@router.message(IsAdminFilter(), AdminBridgeStates.waiting_for_reply_content, F.text)
@router.message(IsAdminFilter(), AdminBridgeStates.waiting_for_info_question, F.text)
async def handle_admin_bridge_send(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    bot: Bot,
) -> None:
    state_data = await state.get_data()
    order_id = state_data.get("bridge_order_id")
    order = await get_order_by_id(session, order_id)

    if not order:
        await message.answer("سفارش مورد نظر یافت نشد.")
        await state.clear()
        return

    admin_msg_text = message.text.strip()
    client_tg_id = order.user.telegram_id

    client_text = texts.CLIENT_RECEIVE_TEAM_MESSAGE.format(
        order_number=order.public_order_number,
        message_text=admin_msg_text,
    )

    try:
        sent = await bot.send_message(
            chat_id=client_tg_id,
            text=client_text,
        )

        client_state_key = StorageKey(
            bot_id=bot.id,
            chat_id=client_tg_id,
            user_id=client_tg_id,
        )
        client_fsm = FSMContext(storage=state.storage, key=client_state_key)
        await client_fsm.set_state(ClientBridgeStates.waiting_for_answer)
        await client_fsm.update_data(bridge_order_id=order.id)

        await save_message(
            session=session,
            user_id=order.user_id,
            sender_type=SenderType.ADMIN,
            sender_id=message.from_user.id,
            content=admin_msg_text,
            order_id=order.id,
            telegram_message_id=sent.message_id,
        )

        await log_admin_action(
            session=session,
            admin_telegram_id=message.from_user.id,
            action="MESSAGE_SENT_TO_CLIENT",
            entity_type="ORDER",
            entity_id=order.id,
            details=f"Admin sent message to client for order #{order.public_order_number}",
        )

        await message.answer(texts.ADMIN_MESSAGE_SENT_SUCCESS)
    except Exception as e:
        await message.answer(f"خطا در ارسال پیام به مشتری: {str(e)}")

    await state.clear()

@router.message(ClientBridgeStates.waiting_for_answer, F.text)
async def handle_client_bridge_answer(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    bot: Bot,
) -> None:
    state_data = await state.get_data()
    order_id = state_data.get("bridge_order_id")
    order = await get_order_by_id(session, order_id)

    client_reply = message.text.strip()
    client_user = await get_user_by_telegram_id(session, message.from_user.id)

    if order and client_user:
        await save_message(
            session=session,
            user_id=client_user.id,
            sender_type=SenderType.CLIENT,
            sender_id=message.from_user.id,
            content=client_reply,
            order_id=order.id,
            telegram_message_id=message.message_id,
        )

        admin_notification = (
            f"📩 پاسخ مشتری به سفارش #{order.public_order_number}\n\n"
            f"👤 مشتری: {message.from_user.full_name} (@{message.from_user.username or 'ندارد'})\n\n"
            f"📝 متن پاسخ:\n"
            f"────────────────\n"
            f"{client_reply}\n"
            f"────────────────"
        )

        for admin_id in settings.ADMIN_IDS:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=admin_notification,
                    reply_markup=get_admin_order_actions_keyboard(order.id),
                )
            except Exception:
                pass

    await state.clear()
    await message.answer(texts.CLIENT_ANSWER_CONFIRMATION)
