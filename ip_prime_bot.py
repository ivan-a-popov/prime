from telegram.ext import Updater, MessageHandler, Filters, InlineQueryHandler, CallbackContext
from telegram import InlineQueryResultArticle, InputTextMessageContent
import logging
import json
import os
from prime import check
import time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

with open('message.json') as file:
    message = json.load(file)

def log(log_message):
    with open('message_log', 'a') as file:
        file.write(time.strftime('%d.%m.%y %H:%M ') + log_message + '\n')


def get_env(name):
    """Reads a required setting from the environment (injected via .env / EnvironmentFile)"""
    try:
        return os.environ[name]
    except KeyError:
        raise SystemExit(f"ERROR: {name} is not set — check the .env file")


TOKEN = get_env('BOT_TOKEN')
MASTER_ID = get_env('MASTER_ID')


def command_process(update, context):
    text = update.message.text
    log('User ' + update.effective_user.first_name + ' ' + update.effective_user.last_name + ' with id ' + str(
        update.effective_user.id) + ' used command ' + text)
    try:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message[text])
    except KeyError:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message['unknown'])


def get_result(query):
    try:
        number = int(query)
        if number <= 0:
            raise ValueError
    except ValueError:
        return query
    else:
        if check(number):
            return query + ' is a prime!'
        else:
            return query + ' is not a prime.'


def answer(update, context):
    text = update.message.text
    log('User ' + update.effective_user.first_name + ' ' + update.effective_user.last_name + ' with id ' + str(
        update.effective_user.id) + ' entered: ' + text)
    result = get_result(text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)


def inline_answer(update, context):
    query = update.inline_query.query
    if not query:
        return
    log('User ' + update.effective_user.first_name + ' ' + update.effective_user.last_name + ' with id ' + str(
        update.effective_user.id) + ' entered: ' + query)
    result = get_result(query)
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query,
            title='Check',
            input_message_content=InputTextMessageContent(result)
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

command_handler = MessageHandler(Filters.command, command_process)
dispatcher.add_handler(command_handler)

answer_handler = MessageHandler(Filters.text & (~Filters.command), answer)
dispatcher.add_handler(answer_handler)

inline_answer_handler = InlineQueryHandler(inline_answer)
dispatcher.add_handler(inline_answer_handler)

updater.start_polling()

job = updater.job_queue


def callback_daily(context: CallbackContext):
    context.bot.send_message(chat_id=MASTER_ID,
                             text="Hi, Master! I'm online.")


job_daily = job.run_repeating(callback_daily, interval=86400, first=10)
