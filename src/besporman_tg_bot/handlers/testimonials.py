from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from besporman_tg_bot.core import texts
from besporman_tg_bot.keyboards.user_kb import (
    get_back_inline_keyboard,
    get_testimonial_keyboard,
)
from besporman_tg_bot.services.testimonial_service import get_random_testimonial

router = Router(name="testimonials")

@router.message(Command("testimonials"))
@router.message(F.text == texts.BTN_TESTIMONIALS)
async def handle_testimonials_menu(message: Message, session: AsyncSession) -> None:
    testimonial = await get_random_testimonial(session)
    if not testimonial:
        await message.answer(
            text=texts.NO_TESTIMONIALS_YET,
            reply_markup=get_back_inline_keyboard(),
        )
        return

    content_text = (
        f"{texts.TESTIMONIAL_INTRO}\n\n"
        f"────────────────\n"
        f"{testimonial.caption or 'رضایت ثبت شده مشتری'}\n"
        f"────────────────\n\n"
        f"{texts.TESTIMONIAL_NEXT_PROMPT}"
    )

    await message.answer(
        text=content_text,
        reply_markup=get_testimonial_keyboard(),
    )

@router.callback_query(F.data == "testim_another")
async def handle_another_testimonial(callback: CallbackQuery, session: AsyncSession) -> None:
    await callback.answer()
    testimonial = await get_random_testimonial(session)
    if not testimonial:
        if callback.message:
            await callback.message.edit_text(
                text=texts.NO_TESTIMONIALS_YET,
                reply_markup=get_back_inline_keyboard(),
            )
        return

    content_text = (
        f"{texts.TESTIMONIAL_INTRO}\n\n"
        f"────────────────\n"
        f"{testimonial.caption or 'رضایت ثبت شده مشتری'}\n"
        f"────────────────\n\n"
        f"{texts.TESTIMONIAL_NEXT_PROMPT}"
    )

    if callback.message:
        await callback.message.edit_text(
            text=content_text,
            reply_markup=get_testimonial_keyboard(),
        )
