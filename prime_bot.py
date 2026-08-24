import logging
import json
import os
import time
from urllib.parse import quote

from dotenv import load_dotenv
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, MessageHandler, InlineQueryHandler, ContextTypes, filters

from prime import check

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, '.env'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

with open(os.path.join(BASE_DIR, 'message.json')) as file:
    message = json.load(file)


def log(log_message):
    with open(os.path.join(BASE_DIR, 'message_log'), 'a') as file:
        file.write(time.strftime('%d.%m.%y %H:%M ') + log_message + '\n')


def get_env(name):
    """Reads a required setting from the environment (loaded from .env)"""
    try:
        return os.environ[name]
    except KeyError:
        raise SystemExit(f"ERROR: {name} is not set — check the .env file")


def build_proxy_url():
    """Optional outbound proxy: TELEGRAM_PROXY as-is, or assembled from PROXY_* parts"""
    explicit = os.getenv('TELEGRAM_PROXY') or os.getenv('HTTPS_PROXY') or os.getenv('ALL_PROXY')
    if explicit:
        return explicit
    host = os.getenv('PROXY_HOST')
    if not host:
        return None
    scheme = os.getenv('PROXY_TYPE', 'socks5').removesuffix('://')
    port = os.getenv('PROXY_PORT', '1080')
    user = os.getenv('PROXY_USER')
    auth = f"{quote(user, safe='')}:{quote(os.getenv('PROXY_PASS') or '', safe='')}@" if user else ''
    return f'{scheme}://{auth}{host}:{port}'


TOKEN = get_env('BOT_TOKEN')
MASTER_ID = get_env('MASTER_ID')
BOT_API_BASE = os.getenv('LOCAL_BOT_API_BASE') or os.getenv('LOCAL_BOT_API')
PROXY_URL = build_proxy_url()


def user_label(user):
    if user is None:
        return 'unknown user'
    return user.first_name + ' ' + (user.last_name or '') + ' with id ' + str(user.id)


def incoming_text(update: Update):
    incoming = update.effective_message
    if incoming is None or not incoming.text:
        return None, None
    return incoming, incoming.text


async def command_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    incoming, text = incoming_text(update)
    if incoming is None:
        return
    log('User ' + user_label(update.effective_user) + ' used command ' + text)
    await incoming.reply_text(message.get(text, message['unknown']))


def get_result(query):
    try:
        number = int(query)
        if number <= 0:
            raise ValueError
    except ValueError:
        return query
    else:
        result = check(number)
        if result is True:
            return query + ' is a prime!'
        if isinstance(result, int):
            return f'{query} is not a prime (divisible by {result}).'
        return query + ' is not a prime.'


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    incoming, text = incoming_text(update)
    if incoming is None:
        return
    log('User ' + user_label(update.effective_user) + ' entered: ' + text)
    await incoming.reply_text(get_result(text))


async def on_non_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    incoming = update.effective_message
    if incoming is None:
        return
    log('User ' + user_label(update.effective_user) + ' sent a non-text message')
    await incoming.reply_text(message['non_text'])


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error('Exception while handling an update', exc_info=context.error)
    incoming = getattr(update, 'effective_message', None)
    if incoming is None:
        return
    try:
        await incoming.reply_text(message['error'])
    except Exception:
        logger.exception('Failed to send error reply')


async def inline_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    log('User ' + user_label(update.effective_user) + ' entered: ' + query)
    results = [
        InlineQueryResultArticle(
            id=query,
            title='Check',
            input_message_content=InputTextMessageContent(get_result(query))
        )
    ]
    await update.inline_query.answer(results)


async def callback_daily(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=MASTER_ID, text="Hi, Master! I'm online.")


def build_application():
    builder = Application.builder().token(TOKEN)
    if BOT_API_BASE:
        api_base = BOT_API_BASE.rstrip('/')
        builder = (
            builder
            .base_url(f'{api_base}/bot')
            .base_file_url(f'{api_base}/file/bot')
            .local_mode(True)
        )
        logger.info('Using local Bot API server at %s', api_base)
    elif PROXY_URL:
        builder = builder.proxy(PROXY_URL).get_updates_proxy(PROXY_URL)
        logger.info('Telegram API proxy enabled: %s', PROXY_URL.rsplit('@', 1)[-1])
    else:
        logger.warning(
            'No LOCAL_BOT_API_BASE or TELEGRAM_PROXY set — '
            'direct connection to api.telegram.org is required'
        )

    application = builder.build()

    application.add_handler(MessageHandler(filters.COMMAND, command_process))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))
    application.add_handler(MessageHandler(~filters.TEXT & ~filters.StatusUpdate.ALL, on_non_text))
    application.add_handler(InlineQueryHandler(inline_answer))
    application.add_error_handler(on_error)

    application.job_queue.run_repeating(callback_daily, interval=86400, first=10)
    return application


def main():
    build_application().run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
