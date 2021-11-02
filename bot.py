import logging

from environs import Env
from telegram.ext import CommandHandler, Updater

from termin_bot.commands import Commands, start_command


def main():
    logging.basicConfig(level=logging.INFO)

    env = Env()
    env.read_env()

    updater = Updater(token=env("BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler(Commands.START, start_command)
    dispatcher.add_handler(start_handler)
    updater.start_polling()


if __name__ == "__main__":
    main()
