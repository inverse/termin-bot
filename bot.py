from pony.orm import db_session
from telegram.ext import CommandHandler, Updater

from termin_bot import common


def main():
    common.bootstrap()
    env = common.get_env()
    updater = Updater(token=env("BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher

    with db_session:
        from termin_bot.commands import (
            Commands,
            command_list,
            command_start,
            command_subscribe,
            command_subscriptions,
            command_uninstall,
            command_unsubscribe,
        )

        dispatcher.add_handler(CommandHandler(Commands.START, command_start))
        dispatcher.add_handler(CommandHandler(Commands.LIST, command_list))
        dispatcher.add_handler(CommandHandler(Commands.SUBSCRIBE, command_subscribe))
        dispatcher.add_handler(
            CommandHandler(Commands.UNSUBSCRIBE, command_unsubscribe)
        )
        dispatcher.add_handler(
            CommandHandler(Commands.SUBSCRIPTIONS, command_subscriptions)
        )
        dispatcher.add_handler(CommandHandler(Commands.UNINSTALL, command_uninstall))
        updater.start_polling()
        updater.idle()


if __name__ == "__main__":
    main()
