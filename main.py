#!/usr/bin/env python3
"""
ImmortalHubKey - Main Entry Point
"""

import asyncio
import logging
import os
from bot import ImmortalHubKeyBot

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main function to run the Discord bot"""
    token = os.getenv("DISCORD_BOT_TOKEN")
    
    if not token:
        logger.error("❌ DISCORD_BOT_TOKEN not found in environment variables.")
        return
    
    bot = ImmortalHubKeyBot()
    
    try:
        logger.info("🚀 Starting ImmortalHubKey Bot...")
        await bot.start(token)
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"⚠️ Error running bot: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
