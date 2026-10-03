from pathlib import Path
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile, Message

from besporman_tg_bot.core import texts
from besporman_tg_bot.keyboards.user_kb import get_team_keyboard

router = Router(name="team")

ASSETS_DIR = Path("assets/resumes")

@router.message(Command("team"))
@router.message(F.text == texts.BTN_TEAM)
async def handle_team_overview(message: Message) -> None:
    content = (
        f"{texts.TEAM_INTRO}\n\n"
        f"👨‍💻 <b>{texts.DEV_1_ALIAS}</b>\n"
        f"🔹 <i>{texts.DEV_1_ROLE}</i>\n"
        f"{texts.DEV_1_BIO}\n\n"
        f"👨‍💻 <b>{texts.DEV_2_ALIAS}</b>\n"
        f"🔹 <i>{texts.DEV_2_ROLE}</i>\n"
        f"{texts.DEV_2_BIO}"
    )
    await message.answer(
        text=content,
        reply_markup=get_team_keyboard(),
        parse_mode="HTML",
    )

@router.callback_query(F.data == "resume_dev1")
async def handle_resume_dev1(callback: CallbackQuery) -> None:
    await callback.answer()
    resume_file = ASSETS_DIR / "resume_dev1.pdf"
    if resume_file.exists():
        if callback.message:
            await callback.message.answer_document(
                document=FSInputFile(str(resume_file)),
                caption=f"📄 رزومه رسمی {texts.DEV_1_ALIAS}",
            )
    else:
        if callback.message:
            await callback.message.answer(
                f"📄 <b>رزومه {texts.DEV_1_ALIAS}</b>\n\n"
                f"تخصص: {texts.DEV_1_ROLE}\n"
                f"{texts.DEV_1_BIO}\n\n"
                f"[PLACEHOLDER: فایل PDF رزومه پس از دریافت از توسعه دهنده بارگذاری می شود.]",
                parse_mode="HTML",
            )

@router.callback_query(F.data == "resume_dev2")
async def handle_resume_dev2(callback: CallbackQuery) -> None:
    await callback.answer()
    resume_file = ASSETS_DIR / "resume_dev2.pdf"
    if resume_file.exists():
        if callback.message:
            await callback.message.answer_document(
                document=FSInputFile(str(resume_file)),
                caption=f"📄 رزومه رسمی {texts.DEV_2_ALIAS}",
            )
    else:
        if callback.message:
            await callback.message.answer(
                f"📄 <b>رزومه {texts.DEV_2_ALIAS}</b>\n\n"
                f"تخصص: {texts.DEV_2_ROLE}\n"
                f"{texts.DEV_2_BIO}\n\n"
                f"[PLACEHOLDER: فایل PDF رزومه پس از دریافت از توسعه دهنده بارگذاری می شود.]",
                parse_mode="HTML",
            )
