"""
Configuration settings for ImmortalHubKey
"""

import os

class BotConfig:
    COMMAND_PREFIX = "!"
    BOT_NAME = "ImmortalHubKey"
    BOT_VERSION = "1.1.0"
    
    MIN_KEY_LENGTH = 4
    MAX_KEY_LENGTH = 64
    DEFAULT_KEY_LENGTH = 16
    MAX_BATCH_SIZE = 10
    
    MAX_EMBED_FIELD_LENGTH = 1024
    MAX_EMBED_DESCRIPTION_LENGTH = 4096
    
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = "bot.log"
    
    RATE_LIMIT_REQUESTS = 5
    RATE_LIMIT_WINDOW = 60
    
    EPHEMERAL_RESPONSES = True
    
    # Guild-specific sync (optional, instant testing)
    GUILD_ID = os.getenv("GUILD_ID")
    
    @classmethod
    def get_bot_token(cls):
        return os.getenv("DISCORD_BOT_TOKEN")
    
    @classmethod
    def validate_config(cls):
        if cls.MIN_KEY_LENGTH >= cls.MAX_KEY_LENGTH:
            raise ValueError("MIN_KEY_LENGTH must be less than MAX_KEY_LENGTH")
        if not (cls.MIN_KEY_LENGTH <= cls.DEFAULT_KEY_LENGTH <= cls.MAX_KEY_LENGTH):
            raise ValueError("DEFAULT_KEY_LENGTH must be valid")
        if cls.MAX_BATCH_SIZE <= 0:
            raise ValueError("MAX_BATCH_SIZE must be > 0")
        return True
