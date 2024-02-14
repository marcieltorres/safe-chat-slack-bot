from src.listeners.messages.regex_message import register as register_regex_message


async def register_listeners(app):
    await register_regex_message(app)
