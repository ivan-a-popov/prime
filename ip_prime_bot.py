from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
start_message = "Привет! Я Prime, бот Ивана Попова. К сожалению, пока что я умею только передразнивать собеседника. " \
                "Но я быстро учусь. :) "
check_message = "All ok, I'm still here."


def get_token(file_name):
    with open(file_name) as file:
        return file.read()[:-1]


TOKEN = get_token('ip_prime_bot_token')


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)


def check(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=check_message)


def echo(update, context):
    with open('messages', 'a') as file:
        file.write(update.message.text+'\n')
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

check_handler = CommandHandler('check', check)
dispatcher.add_handler(check_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
