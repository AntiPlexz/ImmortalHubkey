import discord
from discord.ext import commands
from config import BotConfig
import logging

logger = logging.getLogger("ImmortalHubKey")

class ImmortalHubKeyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(
            command_prefix="!",
            intents=intents,
            application_id=BotConfig.APPLICATION_ID
        )

    async def setup_hook(self):
        # Load all cogs
        await self.load_extension("commands.key_generator")
        await self.load_extension("commands.help")

        try:
            if BotConfig.GUILD_ID:
                guild = discord.Object(id=int(BotConfig.GUILD_ID))
                synced = await self.tree.sync(guild=guild)
                logger.info(f"Synced {len(synced)} command(s) to guild {guild.id}")
            else:
                synced = await self.tree.sync()
                logger.info(f"Synced {len(synced)} global command(s)")
        except Exception as e:
            logger.error(f"Command sync failed: {e}")

    async def on_ready(self):
        logger.info(f"ImmortalHubKey logged in as {self.user} (ID: {self.user.id})")
