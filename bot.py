import logging

from environs import Env
from telegram.ext import CommandHandler, Updater

from termin_bot.commands import Commands, command_help, command_start


def main():
    logging.basicConfig(level=logging.INFO)

    env = Env()
    env.read_env()

    updater = Updater(token=env("BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler(Commands.START, command_start))
    dispatcher.add_handler(CommandHandler(Commands.HELP, command_help))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
