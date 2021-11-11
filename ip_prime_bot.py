from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from math import sqrt
import logging
import json
from prime import check

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

with open('message.json') as file:
    message = json.load(file)


def get_token(file_name):
    with open(file_name) as file:
        return file.read()[:-1]


TOKEN = get_token('ip_prime_bot_token')


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message['start'])


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message['help'])


def ip(update, context):
    with open('message_log', 'a') as file:
        file.write('Someone used ip!\n')
    context.bot.send_message(chat_id=update.effective_chat.id, text=message['ip'])


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message['unknown'])


def get_result(query):
    with open('message_log', 'a') as file:
        file.write(query + '\n')
    try:
        number = int(query)
        if number <= 0:
            raise ValueError
    except ValueError:
        return repr(query)
    else:
        if check(number) and number != 1:
            return 'Yes, ' + query + ' is a prime!'
        else:
            return 'No, ' + query + ' is not a prime.'

def answer(update, context):
    result = get_result(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)


def inline_answer(update, context):
    query = update.inline_query.query
    if not query:
        return
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

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

ip_handler = CommandHandler('ip', ip)
dispatcher.add_handler(ip_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

answer_handler = MessageHandler(Filters.text & (~Filters.command), answer)
dispatcher.add_handler(answer_handler)

inline_answer_handler = InlineQueryHandler(inline_answer)
dispatcher.add_handler(inline_answer_handler)

updater.start_polling()
