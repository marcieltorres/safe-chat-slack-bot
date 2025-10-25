import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.listeners.messages.message_changed import message_changed_callback


@pytest.fixture
def say_mock():
    return AsyncMock()


@pytest.fixture
def event_mock():
    return MagicMock()


@patch('src.listeners.messages.message_changed.pattern')
@patch('src.listeners.messages.message_changed.language')
@pytest.mark.asyncio
async def test_message_changed_with_sensitive_data_triggers_warning(language_mock, pattern_mock, say_mock, event_mock):
    # Arrange
    language_mock.translate.side_effect = lambda x: x  # Mock translation
    pattern_mock.find_all.return_value = 1  # Simulate sensitive data found
    
    # Mock event structure
    event_mock.get.side_effect = lambda key, default=None: {
        'subtype': 'message_changed',
        'message': {
            'text': 'My CPF is 123.456.789-00',
            'user': 'U123456',
            'ts': '1234567890.123456'
        }
    }.get(key, default)
    
    # Mock the 'in' operator for event
    event_mock.__contains__ = lambda key: key in ['subtype', 'message']
    
    # Mock the message object to return the text directly
    message_mock = MagicMock()
    message_mock.get.side_effect = lambda key, default=None: {
        'text': 'My CPF is 123.456.789-00',
        'user': 'U123456',
        'ts': '1234567890.123456'
    }.get(key, default)
    event_mock.__getitem__ = lambda key: message_mock if key == 'message' else event_mock.get(key)

    # Act
    await message_changed_callback(event_mock, say_mock)

    # Assert
    pattern_mock.find_all.assert_called_once_with('My CPF is 123.456.789-00')
    say_mock.assert_called_once()
    call_args = say_mock.call_args
    assert 'Hello' in call_args[1]['text']
    assert 'Do not send sensitive info' in call_args[1]['text']
    assert '<@U123456>' in call_args[1]['text']
    assert call_args[1]['thread_ts'] == '1234567890.123456'


@patch('src.listeners.messages.message_changed.pattern')
@pytest.mark.asyncio
async def test_message_changed_without_sensitive_data_no_warning(pattern_mock, say_mock, event_mock):
    # Arrange
    pattern_mock.find_all.return_value = 0  # No sensitive data found
    
    event_mock.get.side_effect = lambda key, default=None: {
        'subtype': 'message_changed',
        'message': {
            'text': 'Just a regular message',
            'user': 'U123456',
            'ts': '1234567890.123456'
        }
    }.get(key, default)
    
    # Mock the 'in' operator for event
    event_mock.__contains__ = lambda key: key in ['subtype', 'message']
    
    # Mock the message object to return the text directly
    message_mock = MagicMock()
    message_mock.get.side_effect = lambda key, default=None: {
        'text': 'Just a regular message',
        'user': 'U123456',
        'ts': '1234567890.123456'
    }.get(key, default)
    event_mock.__getitem__ = lambda key: message_mock if key == 'message' else event_mock.get(key)

    # Act
    await message_changed_callback(event_mock, say_mock)

    # Assert
    pattern_mock.find_all.assert_called_once_with('Just a regular message')
    say_mock.assert_not_called()


@patch('src.listeners.messages.message_changed.pattern')
@pytest.mark.asyncio
async def test_message_changed_without_subtype_ignored(pattern_mock, say_mock, event_mock):
    # Arrange
    event_mock.get.side_effect = lambda key, default=None: {
        'subtype': 'message_deleted',  # Different subtype
        'message': {
            'text': 'My CPF is 123.456.789-00',
            'user': 'U123456',
            'ts': '1234567890.123456'
        }
    }.get(key, default)
    
    # Mock the 'in' operator for event
    event_mock.__contains__ = lambda key: key in ['subtype', 'message']

    # Act
    await message_changed_callback(event_mock, say_mock)

    # Assert
    pattern_mock.find_all.assert_not_called()
    say_mock.assert_not_called()


@patch('src.listeners.messages.message_changed.pattern')
@pytest.mark.asyncio
async def test_message_changed_without_message_key_ignored(pattern_mock, say_mock, event_mock):
    # Arrange
    event_mock.get.side_effect = lambda key, default=None: {
        'subtype': 'message_changed',
        # No 'message' key
    }.get(key, default)
    
    # Mock the 'in' operator for event - no 'message' key
    event_mock.__contains__ = lambda key: key in ['subtype']

    # Act
    await message_changed_callback(event_mock, say_mock)

    # Assert
    pattern_mock.find_all.assert_not_called()
    say_mock.assert_not_called()


@patch('src.listeners.messages.message_changed.pattern')
@pytest.mark.asyncio
async def test_message_changed_without_user_no_warning(pattern_mock, say_mock, event_mock):
    # Arrange
    pattern_mock.find_all.return_value = 1  # Sensitive data found
    
    event_mock.get.side_effect = lambda key, default=None: {
        'subtype': 'message_changed',
        'message': {
            'text': 'My CPF is 123.456.789-00',
            # No 'user' key
            'ts': '1234567890.123456'
        }
    }.get(key, default)
    
    # Mock the 'in' operator for event
    event_mock.__contains__ = lambda key: key in ['subtype', 'message']
    
    # Mock the message object to return the text directly
    message_mock = MagicMock()
    message_mock.get.side_effect = lambda key, default=None: {
        'text': 'My CPF is 123.456.789-00',
        # No 'user' key
        'ts': '1234567890.123456'
    }.get(key, default)
    event_mock.__getitem__ = lambda key: message_mock if key == 'message' else event_mock.get(key)

    # Act
    await message_changed_callback(event_mock, say_mock)

    # Assert
    pattern_mock.find_all.assert_called_once_with('My CPF is 123.456.789-00')
    say_mock.assert_not_called()


@patch('src.listeners.messages.message_changed.logger')
@patch('src.listeners.messages.message_changed.pattern')
@pytest.mark.asyncio
async def test_message_changed_exception_handling(pattern_mock, logger_mock, say_mock, event_mock):
    # Arrange
    pattern_mock.find_all.side_effect = Exception("Test exception")
    
    event_mock.get.side_effect = lambda key, default=None: {
        'subtype': 'message_changed',
        'message': {
            'text': 'My CPF is 123.456.789-00',
            'user': 'U123456',
            'ts': '1234567890.123456'
        }
    }.get(key, default)
    
    # Mock the 'in' operator for event
    event_mock.__contains__ = lambda key: key in ['subtype', 'message']

    # Act
    await message_changed_callback(event_mock, say_mock)

    # Assert
    logger_mock.error.assert_called_once()
    say_mock.assert_not_called()