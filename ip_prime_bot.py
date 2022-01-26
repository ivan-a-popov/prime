from telegram.ext import Updater, MessageHandler, Filters, InlineQueryHandler, CallbackContext
from telegram import InlineQueryResultArticle, InputTextMessageContent
from math import sqrt
import logging
import json
from prime import check
import time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

with open('message.json') as file:
    message = json.load(file)


def log(log_message):
    with open('message_log', 'a') as file:
        file.write(time.strftime('%d.%m.%y %H:%M ') + log_message + '\n')


def get_token(file_name):
    with open(file_name) as file:
        return file.read()


TOKEN = get_token('bot_token')
MASTER_ID = get_token('master_id')


def command_process(update, context):
    text = update.message.text
    log('User ' + update.effective_user.first_name + ' ' + update.effective_user.last_name + ' with id ' + str(
        update.effective_user.id) + ' used command ' + text + '\n')
    try:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message[text])
    except KeyError:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message['unknown'])


def get_result(query):
    log(query)
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
    result = get_result(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)


def inline_answer(update, context):
    query = update.inline_query.query
    if not query:
        return
    log(query)
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
