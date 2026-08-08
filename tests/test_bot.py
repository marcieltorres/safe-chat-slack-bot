from importlib import import_module
from os import environ
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

# Obviously fake values: importing the module builds a real AsyncApp, which refuses an empty token.
FAKE_ENVIRONMENT = {
    "SLACK_BOT_TOKEN": "xoxb-not-a-real-bot-credential",
    "SLACK_APP_TOKEN": "xapp-not-a-real-app-credential",
}

# logging.conf only sits next to bot.py inside the production image, and the tokens are read at
# import time — so both have to be in place before the module body runs.
with patch("logging.config.fileConfig"), patch.dict(environ, FAKE_ENVIRONMENT):
    bot = import_module("src.bot")


class BotTest(IsolatedAsyncioTestCase):
    def test_tokens_are_read_from_the_environment_with_success(self):
        self.assertEqual(bot.SLACK_BOT_TOKEN, FAKE_ENVIRONMENT["SLACK_BOT_TOKEN"])
        self.assertEqual(bot.SLACK_APP_TOKEN, FAKE_ENVIRONMENT["SLACK_APP_TOKEN"])

    @patch('src.bot.AsyncSocketModeHandler')
    @patch('src.bot.register_listeners', new_callable=AsyncMock)
    async def test_main_registers_the_listeners_with_success(self, register_listeners_mock, handler_mock):
        # Arrange
        handler_mock.return_value.start_async = AsyncMock()

        # Act
        await bot.main()

        # Assert
        register_listeners_mock.assert_awaited_once_with(bot.app)

    @patch('src.bot.AsyncSocketModeHandler')
    @patch('src.bot.register_listeners', new_callable=AsyncMock)
    async def test_main_starts_the_socket_mode_handler_with_success(self, register_listeners_mock, handler_mock):
        # Arrange
        handler_mock.return_value.start_async = AsyncMock()

        # Act
        await bot.main()

        # Assert
        handler_mock.assert_called_once_with(bot.app, bot.SLACK_APP_TOKEN)
        handler_mock.return_value.start_async.assert_awaited_once()

    @patch('src.bot.logger')
    @patch('src.bot.AsyncSocketModeHandler')
    @patch('src.bot.register_listeners', new_callable=AsyncMock)
    async def test_main_logs_the_error_when_the_bot_fails_to_start(
        self, register_listeners_mock, handler_mock, logger_mock
    ):
        # Arrange
        register_listeners_mock.side_effect = Exception("Test exception")

        # Act
        await bot.main()

        # Assert
        handler_mock.assert_not_called()
        logger_mock.error.assert_called_once()
