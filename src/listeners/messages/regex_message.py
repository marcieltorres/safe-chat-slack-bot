from logging import getLogger

from slack_bolt import App

from src.messages.constants import DEFAULT_WARNING_MESSAGE
from src.rules.pattern import pattern

logger = getLogger(__name__)


async def register(app: App):
    app.message(pattern.compiled_pattern)(regex_message_callback)


async def regex_message_callback(message, say):
    try:
        user = message['user']
        await say(text=DEFAULT_WARNING_MESSAGE.format(name=f'<@{user}>'), thread_ts=message.get('ts'))
    except Exception as e:
        logger.error(e)
