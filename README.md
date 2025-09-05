# Arisu-bot

A Discord bot that scrapes a website for changes and reports its status to a Discord channel.

## Features

- Monitors a website for changes.
- Sends updates to a specified Discord channel.
- Keeps track of the last known status between restarts.

## Setup

1. Create a `.env` file with the following variables:
```
    DISCORD_TOKEN=discord_bot_token
    CHANNEL_ID=discord_channel_id_for_alerts
    URL=website_to_monitor
```
2. Install dependencies:

```bash
  pip install -r requirements.txt
```
3. Run the bot:

```bash
  python main.py
```

### Planned Features
- Support for discord slash commands.