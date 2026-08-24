import asyncio
import os
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

os.environ.setdefault('BOT_TOKEN', 'test-token')
os.environ.setdefault('MASTER_ID', '1')

from prime_bot import (  # noqa: E402
    answer,
    command_process,
    incoming_text,
    message,
    on_error,
    on_non_text,
    user_label,
)


def make_user():
    return SimpleNamespace(first_name='Ann', last_name='Bot', id=42)


def make_update(*, text=None, message=True, edited_text=None):
    incoming = None
    if message:
        incoming = SimpleNamespace(text=text, reply_text=AsyncMock())
    edited = None
    if edited_text is not None:
        edited = SimpleNamespace(text=edited_text, reply_text=AsyncMock())
    return SimpleNamespace(
        message=incoming,
        edited_message=edited,
        effective_message=incoming or edited,
        effective_user=make_user(),
    )


def test_user_label_without_user():
    assert user_label(None) == 'unknown user'


def test_incoming_text_without_message():
    update = make_update(message=False)
    assert incoming_text(update) == (None, None)


def test_incoming_text_without_text():
    update = make_update(text=None)
    assert incoming_text(update) == (None, None)


def test_incoming_text_uses_edited_message():
    update = make_update(message=False, edited_text='/help')
    incoming, text = incoming_text(update)
    assert text == '/help'
    assert incoming is update.effective_message


@patch('prime_bot.log')
def test_command_process_ignores_missing_message(mock_log):
    update = make_update(message=False)
    asyncio.run(command_process(update, None))
    mock_log.assert_not_called()


@patch('prime_bot.log')
def test_command_process_ignores_sticker(mock_log):
    update = make_update(text=None)
    asyncio.run(command_process(update, None))
    mock_log.assert_not_called()
    update.effective_message.reply_text.assert_not_called()


@patch('prime_bot.log')
def test_command_process_replies_from_edited_message(mock_log):
    update = make_update(message=False, edited_text='/help')
    asyncio.run(command_process(update, None))
    update.effective_message.reply_text.assert_awaited_once_with(message['/help'])


@patch('prime_bot.log')
def test_answer_ignores_missing_text(mock_log):
    update = make_update(text=None)
    asyncio.run(answer(update, None))
    mock_log.assert_not_called()
    update.effective_message.reply_text.assert_not_called()


@patch('prime_bot.log')
def test_on_non_text_explains_sticker(mock_log):
    update = make_update(text=None)
    asyncio.run(on_non_text(update, None))
    update.effective_message.reply_text.assert_awaited_once_with(message['non_text'])
    mock_log.assert_called_once()


@patch('prime_bot.log')
def test_on_non_text_without_message(mock_log):
    update = make_update(message=False)
    asyncio.run(on_non_text(update, None))
    mock_log.assert_not_called()


def test_on_error_replies_and_logs():
    incoming = SimpleNamespace(reply_text=AsyncMock())
    update = SimpleNamespace(effective_message=incoming)
    context = SimpleNamespace(error=RuntimeError('boom'))
    with patch('prime_bot.logger.error') as mock_error:
        asyncio.run(on_error(update, context))
    incoming.reply_text.assert_awaited_once_with(message['error'])
    mock_error.assert_called_once()


def test_on_error_without_update():
    context = SimpleNamespace(error=RuntimeError('boom'))
    with patch('prime_bot.logger.error'):
        asyncio.run(on_error(None, context))


def test_on_error_reply_failure_is_swallowed():
    incoming = SimpleNamespace(reply_text=AsyncMock(side_effect=RuntimeError('send failed')))
    update = SimpleNamespace(effective_message=incoming)
    context = SimpleNamespace(error=RuntimeError('boom'))
    with patch('prime_bot.logger.error'), patch('prime_bot.logger.exception') as mock_exception:
        asyncio.run(on_error(update, context))
    mock_exception.assert_called_once()
