from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from src.listeners.register import register_listeners


class RegisterListenersTest(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.app_mock = MagicMock()

    @patch('src.listeners.register.register_message_changed', new_callable=AsyncMock)
    @patch('src.listeners.register.register_regex_message', new_callable=AsyncMock)
    async def test_register_regex_message_listener_with_success(self, regex_message_mock, message_changed_mock):
        # Act
        await register_listeners(self.app_mock)

        # Assert
        regex_message_mock.assert_awaited_once_with(self.app_mock)

    @patch('src.listeners.register.register_message_changed', new_callable=AsyncMock)
    @patch('src.listeners.register.register_regex_message', new_callable=AsyncMock)
    async def test_register_message_changed_listener_with_success(self, regex_message_mock, message_changed_mock):
        # Act
        await register_listeners(self.app_mock)

        # Assert
        message_changed_mock.assert_awaited_once_with(self.app_mock)
