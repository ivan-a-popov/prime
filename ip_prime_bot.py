from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from math import sqrt
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

start_message = "Hi! I'm Prime bot. I can check the numbers for the primality.\n" \
                "Unfortunately, that's all I can do meanwhile,\n" \
                "but I'll probably learn something else in the future. :)"

help_message = "Type a natural number (positive integer, i.e. 1 and greater), and I'll check if it's a prime.\n" \
               "If you type anything except a valid number, I'll just repeat your message."

ip_message = "Oh, ip means a lot for me! IP stands for Ivan Popov.\n" \
             "Ivan Popov is my Lord, my Master, my Creator!\n" \
             "He is the best man I know! Well, actually, he's the only one..."


def get_token(file_name):
    with open(file_name) as file:
        return file.read()[:-1]


TOKEN = get_token('ip_prime_bot_token')


def check(number):
    """Base function, checks if number us a prime. Returns True if it is, False otherwise.

    Using the square root reduces the time needed for check drastically:
    If there's no divisor of N between 1 and sqrt(N)+1, there's just no sense in searching above.
    (See https://en.wikipedia.org/wiki/Prime_number#Trial_division for details.)
    """

    if number == 2:
        return True
    if number % 2 == 0:
        return False
    # I know this looks ugly, but excluding evens halves the quantity of checks in total, and 2 itself is a prime
    for divisor in range(3, int(sqrt(number) + 1), 2):
        if number % divisor == 0:
            return False
    else:
        return True


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)


def ip(update, context):
    with open('messages', 'a') as file:
        file.write('Someone used ip!\n')
    context.bot.send_message(chat_id=update.effective_chat.id, text=ip_message)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I don't understand that command.")


def answer(update, context):
    with open('messages', 'a') as file:
        file.write(update.message.text+'\n')
    try:
        number = int(update.message.text)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    else:
        if check(number):
            context.bot.send_message(chat_id=update.effective_chat.id, text='Yes, '+update.message.text+' is a prime.')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='No, '+update.message.text+' is not a prime.')


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
