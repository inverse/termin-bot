import logging

from environs import Env
from telegram.ext import CommandHandler, Updater

logging.basicConfig(level=logging.INFO)

env = Env()
env.read_env()

updater = Updater(token=env("BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)
updater.start_polling()
