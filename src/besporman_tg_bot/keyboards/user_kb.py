from typing import List, Optional
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from besporman_tg_bot.core import texts
from besporman_tg_bot.db.models import Portfolio

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=texts.BTN_ORDER)],
        [KeyboardButton(text=texts.BTN_SERVICES), KeyboardButton(text=texts.BTN_PORTFOLIO)],
        [KeyboardButton(text=texts.BTN_TESTIMONIALS), KeyboardButton(text=texts.BTN_TEAM)],
        [KeyboardButton(text=texts.BTN_SUPPORT)],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )

def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=texts.BTN_CANCEL)]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_back_inline_keyboard(callback_data: str = "nav_main_menu") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=texts.BTN_BACK, callback_data=callback_data)]]
    )

def get_services_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=texts.BTN_SERVICE_ORDER, callback_data="order_start")],
        [InlineKeyboardButton(text=texts.BTN_BACK, callback_data="nav_main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_portfolio_list_keyboard(items: List[Portfolio]) -> InlineKeyboardMarkup:
    buttons = []
    for item in items:
        buttons.append([InlineKeyboardButton(text=item.title, callback_data=f"port_detail:{item.id}")])

    buttons.append([InlineKeyboardButton(text=texts.BTN_BACK, callback_data="nav_main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_portfolio_detail_keyboard(
    current_id: int,
    prev_id: Optional[int] = None,
    next_id: Optional[int] = None,
) -> InlineKeyboardMarkup:
    keyboard = []
    nav_row = []
    if prev_id is not None:
        nav_row.append(InlineKeyboardButton(text=texts.BTN_PREV_PROJECT, callback_data=f"port_detail:{prev_id}"))
    if next_id is not None:
        nav_row.append(InlineKeyboardButton(text=texts.BTN_NEXT_PROJECT, callback_data=f"port_detail:{next_id}"))

    if nav_row:
        keyboard.append(nav_row)

    keyboard.append([InlineKeyboardButton(text=texts.BTN_ORDER_SIMILAR, callback_data=f"order_similar:{current_id}")])
    keyboard.append([InlineKeyboardButton(text=texts.BTN_BACK_TO_PORTFOLIO, callback_data="port_list")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_testimonial_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=texts.BTN_ANOTHER_TESTIMONIAL, callback_data="testim_another")],
        [InlineKeyboardButton(text=texts.BTN_START_MY_PROJECT, callback_data="order_start")],
        [InlineKeyboardButton(text=texts.BTN_BACK, callback_data="nav_main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_team_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=texts.BTN_RESUME_DEV1, callback_data="resume_dev1")],
        [InlineKeyboardButton(text=texts.BTN_RESUME_DEV2, callback_data="resume_dev2")],
        [InlineKeyboardButton(text=texts.BTN_ORDER, callback_data="order_start")],
        [InlineKeyboardButton(text=texts.BTN_BACK, callback_data="nav_main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
