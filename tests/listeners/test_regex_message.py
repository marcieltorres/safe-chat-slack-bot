from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from src.listeners.messages.regex_message import regex_message_callback, register


class RegexMessageTest(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.say_mock = AsyncMock()
        self.message = {'user': 'U123456', 'ts': '1234567890.123456'}

    @patch('src.listeners.messages.regex_message.pattern')
    async def test_register_wires_the_callback_to_the_compiled_pattern_with_success(self, pattern_mock):
        # Arrange
        app_mock = MagicMock()

        # Act
        await register(app_mock)

        # Assert
        app_mock.message.assert_called_once_with(pattern_mock.compiled_pattern)
        app_mock.message.return_value.assert_called_once_with(regex_message_callback)

    @patch('src.listeners.messages.regex_message.language')
    async def test_callback_replies_in_thread_with_success(self, language_mock):
        # Arrange
        language_mock.translate.side_effect = lambda key: key

        # Act
        await regex_message_callback(self.message, self.say_mock)

        # Assert
        self.say_mock.assert_awaited_once()
        call_args = self.say_mock.call_args
        self.assertIn('<@U123456>', call_args[1]['text'])
        self.assertEqual(call_args[1]['thread_ts'], '1234567890.123456')

    @patch('src.listeners.messages.regex_message.language')
    async def test_callback_builds_the_warning_from_the_translations_with_success(self, language_mock):
        # Arrange
        language_mock.translate.side_effect = lambda key: f'[{key}]'

        # Act
        await regex_message_callback(self.message, self.say_mock)

        # Assert
        self.assertEqual(self.say_mock.call_args[1]['text'], '[Hello] <@U123456>, [Do not send sensitive info]')

    @patch('src.listeners.messages.regex_message.logger')
    async def test_callback_logs_the_exception_when_the_message_has_no_user(self, logger_mock):
        # Act
        await regex_message_callback({'ts': '1234567890.123456'}, self.say_mock)

        # Assert
        logger_mock.error.assert_called_once()
        self.assertIsInstance(logger_mock.error.call_args[0][0], KeyError)
        self.say_mock.assert_not_awaited()
