# Cryptohopper Trade Logger Bot

Python Telegram bot that:
- Listens for trade messages (buy/sell/hop) from the Cryptohopper Bot.
- Logs them to a local JSON file.
- Forwards them to a personal bot, channel, or group.

## ✅ Features

- ✅ No Telegram API ID required.
- ✅ Uses only your Bot Token.
- ✅ Easy to deploy.

## 📦 Requirements

```bash
pip install python-telegram-bot
```

## ⚙️ Setup

1. Get a bot token from [@BotFather](https://t.me/BotFather).
2. Create a Telegram group and add both:
   - Your bot (make it an admin).
   - `@Cryptohopper_Bot`.
3. Edit the following lines in `simple_cryptohopper_logger.py`:

```python
BOT_TOKEN = 'YOUR_BOT_TOKEN'
TARGET_CHAT_ID = '@your_channel_or_group'
```

4. Run the bot:

```bash
python simple_cryptohopper_logger.py
```

## 🗃 Logs

Trade messages are saved to `trades.json` for backup and review.

## 🛡 License

MIT
