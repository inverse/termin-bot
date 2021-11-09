import click


@click.group()
def cli():
    pass


@cli.command()
def process_subscriptions():
    """Process subscriptions."""
    click.echo("Processing subscriptions")


if __name__ == "__main__":
    cli()
