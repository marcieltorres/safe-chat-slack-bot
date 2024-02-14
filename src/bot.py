from asyncio import run as async_run
from logging import getLogger
from logging.config import fileConfig as logConfig
from os import getenv

from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp

from src.listeners.register import register_listeners

logConfig("./logging.conf", disable_existing_loggers=False)
logger = getLogger(__name__)

SLACK_BOT_TOKEN = getenv("SLACK_BOT_TOKEN", "").strip()
SLACK_APP_TOKEN = getenv("SLACK_APP_TOKEN", "").strip()

app = AsyncApp(token=SLACK_BOT_TOKEN)

async def main():
    try:
        await register_listeners(app)
        handler = AsyncSocketModeHandler(app, SLACK_APP_TOKEN)
        await handler.start_async()
    except Exception as ex:
        logger.error("Error when starting the bot", ex)

if __name__ == "__main__":  # pragma: no cover
    async_run(main())
