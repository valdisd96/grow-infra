import os
FUN_RELAY_PIN = int(os.environ.get("FUN_RELAY_PIN", 6))
LIGHT_RELAY_PIN = int(os.environ.get("LIGHT_RELAY_PIN", 5))
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "token")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "chat_id")