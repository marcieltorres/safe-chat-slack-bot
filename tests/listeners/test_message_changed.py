from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from src.listeners.messages.message_changed import message_changed_callback, register


class MessageChangedTest(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.say_mock = AsyncMock()
        self.event_mock = MagicMock()

    @patch('src.listeners.messages.message_changed.pattern')
    @patch('src.listeners.messages.message_changed.language')
    async def test_message_changed_with_sensitive_data_triggers_warning(self, language_mock, pattern_mock):
        # Arrange
        language_mock.translate.side_effect = lambda key: {
            "Hello": "Hello",
            "Do not send sensitive info": "Do not send sensitive info"
        }.get(key, key)
        pattern_mock.find_all.return_value = 1  # Simulate sensitive data found

        # Create mock message data
        message_data = {
            'text': 'My CPF is 123.456.789-00',
            'user': 'U123456',
            'ts': '1234567890.123456'
        }

        # Configure event mock to behave like a dict
        self.event_mock.get.return_value = None
        def event_get(key, default=None):
            if key == 'subtype':
                return 'message_changed'
            elif key == 'message':
                return message_data
            return default
        self.event_mock.get.side_effect = event_get
        self.event_mock.__contains__.side_effect = lambda key: key in ['subtype', 'message']
        self.event_mock.__getitem__.side_effect = lambda key: message_data if key == 'message' else None

        # Act
        await message_changed_callback(self.event_mock, self.say_mock)

        # Assert
        pattern_mock.find_all.assert_called_once_with('My CPF is 123.456.789-00')
        self.say_mock.assert_called_once()
        call_args = self.say_mock.call_args
        self.assertIn('Hello', call_args[1]['text'])
        self.assertIn('Do not send sensitive info', call_args[1]['text'])
        self.assertIn('<@U123456>', call_args[1]['text'])
        self.assertEqual(call_args[1]['thread_ts'], '1234567890.123456')

    @patch('src.listeners.messages.message_changed.pattern')
    async def test_message_changed_without_sensitive_data_no_warning(self, pattern_mock):
        # Arrange
        pattern_mock.find_all.return_value = 0  # No sensitive data found

        # Create mock message data
        message_data = {
            'text': 'Just a regular message',
            'user': 'U123456',
            'ts': '1234567890.123456'
        }

        # Configure event mock to behave like a dict
        self.event_mock.get.return_value = None
        def event_get(key, default=None):
            if key == 'subtype':
                return 'message_changed'
            elif key == 'message':
                return message_data
            return default
        self.event_mock.get.side_effect = event_get
        self.event_mock.__contains__.side_effect = lambda key: key in ['subtype', 'message']
        self.event_mock.__getitem__.side_effect = lambda key: message_data if key == 'message' else None

        # Act
        await message_changed_callback(self.event_mock, self.say_mock)

        # Assert
        pattern_mock.find_all.assert_called_once_with('Just a regular message')
        self.say_mock.assert_not_called()

    @patch('src.listeners.messages.message_changed.pattern')
    async def test_message_changed_without_subtype_ignored(self, pattern_mock):
        # Arrange
        self.event_mock.get.side_effect = lambda key, default=None: {
            'subtype': 'message_deleted',  # Different subtype
            'message': {
                'text': 'My CPF is 123.456.789-00',
                'user': 'U123456',
                'ts': '1234567890.123456'
            }
        }.get(key, default)

        # Mock the 'in' operator for event
        self.event_mock.__contains__ = lambda key: key in ['subtype', 'message']

        # Act
        await message_changed_callback(self.event_mock, self.say_mock)

        # Assert
        pattern_mock.find_all.assert_not_called()
        self.say_mock.assert_not_called()

    @patch('src.listeners.messages.message_changed.pattern')
    async def test_message_changed_without_message_key_ignored(self, pattern_mock):
        # Arrange
        self.event_mock.get.side_effect = lambda key, default=None: {
            'subtype': 'message_changed',
            # No 'message' key
        }.get(key, default)

        # Mock the 'in' operator for event - no 'message' key
        self.event_mock.__contains__ = lambda key: key in ['subtype']

        # Act
        await message_changed_callback(self.event_mock, self.say_mock)

        # Assert
        pattern_mock.find_all.assert_not_called()
        self.say_mock.assert_not_called()

    @patch('src.listeners.messages.message_changed.pattern')
    async def test_message_changed_without_user_no_warning(self, pattern_mock):
        # Arrange
        pattern_mock.find_all.return_value = 1  # Sensitive data found

        # Create mock message data without 'user'
        message_data = {
            'text': 'My CPF is 123.456.789-00',
            'ts': '1234567890.123456'
            # No 'user' key
        }

        # Configure event mock to behave like a dict
        self.event_mock.get.return_value = None
        def event_get(key, default=None):
            if key == 'subtype':
                return 'message_changed'
            elif key == 'message':
                return message_data
            return default
        self.event_mock.get.side_effect = event_get
        self.event_mock.__contains__.side_effect = lambda key: key in ['subtype', 'message']
        self.event_mock.__getitem__.side_effect = lambda key: message_data if key == 'message' else None

        # Act
        await message_changed_callback(self.event_mock, self.say_mock)

        # Assert
        pattern_mock.find_all.assert_called_once_with('My CPF is 123.456.789-00')
        self.say_mock.assert_not_called()

    @patch('src.listeners.messages.message_changed.logger')
    @patch('src.listeners.messages.message_changed.pattern')
    async def test_message_changed_exception_handling(self, pattern_mock, logger_mock):
        # Arrange
        pattern_mock.find_all.side_effect = Exception("Test exception")

        self.event_mock.get.side_effect = lambda key, default=None: {
            'subtype': 'message_changed',
            'message': {
                'text': 'My CPF is 123.456.789-00',
                'user': 'U123456',
                'ts': '1234567890.123456'
            }
        }.get(key, default)

        # Mock the 'in' operator for event
        self.event_mock.__contains__ = lambda key: key in ['subtype', 'message']

        # Act
        await message_changed_callback(self.event_mock, self.say_mock)

        # Assert
        logger_mock.error.assert_called_once()
        self.say_mock.assert_not_called()

    async def test_register_function(self):
        # Arrange
        app_mock = MagicMock()

        # Act
        await register(app_mock)

        # Assert
        app_mock.event.assert_called_once_with("message")
        app_mock.event.return_value.assert_called_once_with(message_changed_callback)
