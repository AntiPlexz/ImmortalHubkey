"""
ImmortalHubKey - Main Bot Class
"""

import discord
from discord.ext import commands
import logging
from config import BotConfig
from commands.key_generator import KeyGeneratorCog

logger = logging.getLogger(__name__)

class ImmortalHubKeyBot(commands.Bot):
    """Main bot class for ImmortalHubKey"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = False  # Slash-only bot
        
        super().__init__(
            command_prefix=BotConfig.COMMAND_PREFIX,
            intents=intents,
            help_command=None
        )
        
    async def setup_hook(self):
        """Set up the bot when it starts"""
        await self.add_cog(KeyGeneratorCog(self))
        
        # Sync slash commands (guild if provided, else global)
        try:
            if BotConfig.GUILD_ID:
                guild = discord.Object(id=int(BotConfig.GUILD_ID))
                synced = await self.tree.sync(guild=guild)
                logger.info(f"🔧 Synced {len(synced)} command(s) to guild {BotConfig.GUILD_ID}")
            else:
                synced = await self.tree.sync()
                logger.info(f"🔧 Synced {len(synced)} global command(s)")
        except Exception as e:
            logger.error(f"❌ Failed to sync commands: {e}")
    
    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f"✅ {self.user} is online in {len(self.guilds)} guild(s)")
        
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="for /generate-key"
        )
        await self.change_presence(activity=activity)
    
    async def on_command_error(self, ctx, error):
        """Handle command errors"""
        if isinstance(error, commands.CommandNotFound):
            return
        logger.error(f"⚠️ Command error: {error}")
        await ctx.send("❌ An error occurred. Use `/key-help` for usage.")
