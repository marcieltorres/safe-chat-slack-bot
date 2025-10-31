from src.listeners.messages.regex_message import register as register_regex_message
from src.listeners.messages.message_changed import register as register_message_changed


async def register_listeners(app):
    await register_regex_message(app)
    await register_message_changed(app)
