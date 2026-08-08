from json import dumps
from os import environ
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from slack_bolt.async_app import AsyncApp
from slack_bolt.request.async_request import AsyncBoltRequest
from slack_sdk.web.async_client import AsyncWebClient

from src.listeners.register import register_listeners

# Obviously fake values: no real credential, workspace or person is referenced here.
FAKE_ENVIRONMENT = {"SLACK_BOT_TOKEN": "xoxb-not-a-real-bot-credential"}
FAKE_CPF = '000.000.000-00'
BOT_USER_ID = 'U000BOT'
CHANNEL_ID = 'C000000'
USER_ID = 'U000000'
MESSAGE_TS = '1700000000.000100'
EVENT_TS = '1700000000.000200'


def build_event_request(event: dict) -> AsyncBoltRequest:
    body = {
        'team_id': 'T000000',
        'api_app_id': 'A000000',
        'type': 'event_callback',
        'event_id': 'Ev000000',
        'event_time': 1700000000,
        'event': event,
    }
    return AsyncBoltRequest(body=dumps(body), headers={'content-type': ['application/json']})


def build_new_message_event(text: str) -> dict:
    return {
        'type': 'message',
        'channel': CHANNEL_ID,
        'channel_type': 'channel',
        'user': USER_ID,
        'text': text,
        'ts': MESSAGE_TS,
        'event_ts': MESSAGE_TS,
    }


def build_edited_message_event(text: str) -> dict:
    return {
        'type': 'message',
        'subtype': 'message_changed',
        'channel': CHANNEL_ID,
        'channel_type': 'channel',
        'ts': EVENT_TS,
        'event_ts': EVENT_TS,
        'message': {'type': 'message', 'user': USER_ID, 'text': text, 'ts': MESSAGE_TS},
        'previous_message': {'type': 'message', 'user': USER_ID, 'text': 'nothing to see here', 'ts': MESSAGE_TS},
    }


class MessageFlowTest(IsolatedAsyncioTestCase):
    """Drives a synthetic Slack event through a real AsyncApp: registration, matching, detection and
    reply. Nothing is mocked below the Slack web client, so the real pattern engine runs."""

    async def asyncSetUp(self) -> None:
        auth_test_result = MagicMock()
        auth_test_result.get.side_effect = {
            'user_id': BOT_USER_ID,
            'team_id': 'T000000',
            'bot_id': 'B000000',
        }.get
        auth_test_result.headers = {'x-oauth-scopes': 'chat:write'}

        self.post_message_mock = self.patch_web_client('chat_postMessage', AsyncMock())
        self.patch_web_client('auth_test', AsyncMock(return_value=auth_test_result))

        # process_before_response makes async_dispatch await the listeners instead of scheduling them,
        # so the assertions below do not race the event loop.
        with patch.dict(environ, FAKE_ENVIRONMENT):
            self.app = AsyncApp(request_verification_enabled=False, process_before_response=True)
        await register_listeners(self.app)

    def patch_web_client(self, method: str, replacement: AsyncMock) -> AsyncMock:
        patcher = patch.object(AsyncWebClient, method, new=replacement)
        self.addCleanup(patcher.stop)
        return patcher.start()

    async def test_new_message_with_sensitive_data_is_answered_in_thread_with_success(self):
        # Act
        response = await self.app.async_dispatch(build_event_request(build_new_message_event(f'meu {FAKE_CPF}')))

        # Assert
        self.assertEqual(response.status, 200)
        self.post_message_mock.assert_awaited_once()
        call_args = self.post_message_mock.call_args
        self.assertEqual(call_args[1]['channel'], CHANNEL_ID)
        self.assertEqual(call_args[1]['thread_ts'], MESSAGE_TS)
        self.assertIn(f'<@{USER_ID}>', call_args[1]['text'])

    async def test_new_message_without_sensitive_data_is_ignored_with_success(self):
        # Act
        response = await self.app.async_dispatch(build_event_request(build_new_message_event('bom dia a todos')))

        # Assert
        self.assertEqual(response.status, 200)
        self.post_message_mock.assert_not_awaited()

    async def test_edited_message_with_sensitive_data_is_answered_in_thread_with_success(self):
        # Act
        response = await self.app.async_dispatch(build_event_request(build_edited_message_event(f'meu {FAKE_CPF}')))

        # Assert
        self.assertEqual(response.status, 200)
        self.post_message_mock.assert_awaited_once()
        call_args = self.post_message_mock.call_args
        self.assertEqual(call_args[1]['thread_ts'], MESSAGE_TS)
        self.assertIn(f'<@{USER_ID}>', call_args[1]['text'])

    async def test_edited_message_without_sensitive_data_is_ignored_with_success(self):
        # Act
        response = await self.app.async_dispatch(build_event_request(build_edited_message_event('bom dia a todos')))

        # Assert
        self.assertEqual(response.status, 200)
        self.post_message_mock.assert_not_awaited()
