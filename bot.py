import logging
from os.path import abspath

from environs import Env
from pony.orm import db_session
from telegram.ext import CommandHandler, Updater

from termin_bot.commands import Commands, command_help, command_start, command_list
from termin_bot.models import (Termin, User, find_user_termins,
                               find_users_for_termin_type, setup_database)


def main():
    logging.basicConfig(level=logging.INFO)

    env = Env()
    env.read_env()

    setup_database(abspath(env("DB_PATH")))

    updater = Updater(token=env("BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler(Commands.START, command_start))
    dispatcher.add_handler(CommandHandler(Commands.HELP, command_help))
    dispatcher.add_handler(CommandHandler(Commands.LIST, command_list))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
