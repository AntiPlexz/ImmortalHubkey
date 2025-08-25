import os

class BotConfig:
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    APPLICATION_ID = int(os.getenv("APPLICATION_ID", "0")) or None
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    EPHEMERAL_RESPONSES = os.getenv("EPHEMERAL_RESPONSES", "true").lower() == "true"
    GUILD_ID = os.getenv("GUILD_ID")  # Optional: for instant slash sync
