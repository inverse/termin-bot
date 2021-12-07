# Berlin Termin Bot (WIP)

A Telegram bot for helping finding a Termin on the Berlin services website.

You can interact with the production bot at `@TBD`

## Development

Create a Telegram bot following the [official documentation](https://core.telegram.org/bots#3-how-do-i-create-a-bot).

Copy `.env.example` to `.env` and provide your newly created bot token in `BOT_TOKEN`, as well as configuring a suitable path for the persistance layer.

### Bot

You can start the bot using:

```bash
python cli.py bot
```

### Scraping

Scrape appointments using:

```bash
python cli.py scrape-appointments
```

### Processing

Process subscriptions using:

```bash
python cli.py process-subscriptions
```

You will probably want to run this on some cron schedule as this is what will be scraping the appointments and sending notifications.
