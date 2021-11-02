from telegram import Update
from telegram.ext.utils.types import CCT


class Commands:
    START = "start"


def start_command(update: Update, context: CCT):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )
