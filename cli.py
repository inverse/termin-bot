import click

from termin_bot import appointment_handler, common, model, scraper


@click.group()
def cli():
    pass


@cli.command()
def scrape_appointments():
    """Scrape available appointments."""
    click.echo("Started scraping appointments")
    appointments = scraper.scrape_appointments()
    model.update_appointments(appointments)
    click.echo("Finished scraping  appointments")


@cli.command()
def process_subscriptions():
    """Process subscriptions."""
    click.echo("Started processing subscriptions")
    appointment_handler.handle_appointments(model.find_appointments())
    click.echo("Finished processing subscriptions")


if __name__ == "__main__":
    common.bootstrap()
    cli()
