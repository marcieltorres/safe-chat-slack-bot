from logging import getLogger

from slack_bolt import App

from src.config.language import language
from src.rules.pattern import pattern

logger = getLogger(__name__)


async def register(app: App):
    app.message(pattern.compiled_pattern)(regex_message_callback)


async def regex_message_callback(message, say):
    try:
        user = message['user']
        text = f'{language.translate("Hello")} <@{user}>, {language.translate("Do not send sensitive info")}'
        await say(text=text, thread_ts=message.get('ts'))
    except Exception as e:
        logger.error(e)
