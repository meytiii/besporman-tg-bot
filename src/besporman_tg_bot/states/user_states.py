from aiogram.fsm.state import State, StatesGroup

class OrderStates(StatesGroup):
    waiting_for_description = State()

class SupportStates(StatesGroup):
    waiting_for_message = State()

class AdminBridgeStates(StatesGroup):
    waiting_for_reply_content = State()
    waiting_for_info_question = State()

class ClientBridgeStates(StatesGroup):
    waiting_for_answer = State()
