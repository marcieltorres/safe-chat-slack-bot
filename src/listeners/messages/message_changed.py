from logging import getLogger

from slack_bolt import App

from src.config.language import language
from src.rules.pattern import pattern

logger = getLogger(__name__)


async def register(app: App):
    app.event("message")(message_changed_callback)


async def message_changed_callback(event, say):
    try:
        # Check if this is a message_changed event with edited text
        if event.get("subtype") == "message_changed" and "message" in event:
            edited_message = event["message"]
            text = edited_message.get("text", "")

            # Check if the edited message contains sensitive data
            if pattern.find_all(text) > 0:
                user = edited_message.get("user")
                if user:
                    warning_text = (
                        f'{language.translate("Hello")} <@{user}>, '
                        f'{language.translate("Do not send sensitive info")}'
                    )
                    await say(text=warning_text, thread_ts=edited_message.get("ts"))
    except Exception as e:
        logger.error(e)