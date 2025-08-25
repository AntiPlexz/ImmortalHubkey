from bot import ImmortalHubKeyBot
from config import BotConfig
import logging

logging.basicConfig(level=getattr(logging, BotConfig.LOG_LEVEL, logging.INFO))
logger = logging.getLogger("ImmortalHubKey")

if __name__ == "__main__":
    bot = ImmortalHubKeyBot()
    try:
        logger.info("Starting ImmortalHubKey...")
        bot.run(BotConfig.TOKEN)
    except Exception as e:
        logger.error(f"Bot stopped due to error: {e}")
