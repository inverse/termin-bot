import click
from pony.orm import db_session
from telegram.ext import CommandHandler, Updater

from termin_bot import appointment_handler, common, model, scraper


@click.group()
def cli():
    pass


@cli.command()
@db_session
def bot():
    """Start the bot"""
    env = common.get_env()
    updater = Updater(token=env("BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher

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


@cli.command()
@db_session
def scrape_appointments():
    """Scrape available appointments."""
    click.echo("Started scraping appointments")
    appointments = scraper.scrape_appointments()
    model.update_appointments(appointments)
    click.echo("Finished scraping  appointments")


@cli.command()
@db_session
def process_subscriptions():
    """Process subscriptions."""
    click.echo("Started processing subscriptions")
    appointment_handler.handle_appointments(model.find_appointments())
    click.echo("Finished processing subscriptions")


if __name__ == "__main__":
    common.bootstrap()
    cli()
