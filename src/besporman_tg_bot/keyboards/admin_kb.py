from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from besporman_tg_bot.core import texts
from besporman_tg_bot.db.models import OrderStatus

def get_admin_order_actions_keyboard(order_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text=texts.BTN_ADMIN_REPLY, callback_data=f"adm_reply:{order_id}"),
            InlineKeyboardButton(text=texts.BTN_ADMIN_REQUEST_INFO, callback_data=f"adm_ask:{order_id}"),
        ],
        [
            InlineKeyboardButton(text=texts.BTN_ADMIN_CHANGE_STATUS, callback_data=f"adm_status_menu:{order_id}"),
        ],
        [
            InlineKeyboardButton(text=texts.BTN_ADMIN_ACCEPT, callback_data=f"adm_quick_status:{order_id}:{OrderStatus.ACCEPTED}"),
            InlineKeyboardButton(text=texts.BTN_ADMIN_REJECT, callback_data=f"adm_quick_status:{order_id}:{OrderStatus.REJECTED}"),
        ],
        [
            InlineKeyboardButton(text=texts.BTN_ADMIN_CLOSE, callback_data=f"adm_quick_status:{order_id}:{OrderStatus.CLOSED}"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_admin_status_selection_keyboard(order_id: int) -> InlineKeyboardMarkup:
    keyboard = []
    for status_key, label in texts.STATUS_LABELS.items():
        keyboard.append([
            InlineKeyboardButton(
                text=label,
                callback_data=f"adm_set_status:{order_id}:{status_key}",
            )
        ])

    keyboard.append([
        InlineKeyboardButton(text="🔙 بازگشت به سفارش", callback_data=f"adm_view_order:{order_id}")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_admin_dashboard_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="🚨 سفارش های جدید", callback_data="adm_list:NEW"),
            InlineKeyboardButton(text="📋 سفارش های فعال", callback_data="adm_list:ACTIVE"),
        ],
        [
            InlineKeyboardButton(text="📊 آمار ربات", callback_data="adm_stats"),
            InlineKeyboardButton(text="📜 لاگ های اخیر", callback_data="adm_audit_logs"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_admin_cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="❌ انصراف", callback_data="adm_cancel")]]
    )
