from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
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


def answer(update, context):
    with open('message_log', 'a') as file:
        file.write(update.message.text+'\n')
    try:
        number = int(update.message.text)
        if number % 2 != 0 and len(update.message.text) >= 18:
            context.bot.send_message(chat_id=update.effective_chat.id, text=message['huge'])
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    else:
        if check(number):
            result = 'Yes, '+update.message.text+' is a prime!'
        else:
            result = 'No, '+update.message.text+' is not a prime.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=result)


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

updater.start_polling()
