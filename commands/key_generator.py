import discord
from discord import app_commands
from discord.ext import commands
import random, string, uuid
from config import BotConfig

CHARSETS = {
    "alphanumeric": string.ascii_letters + string.digits,
    "hex": string.hexdigits.lower(),
    "numeric": string.digits,
}

class KeyGenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def generate_key(self, length: int, format_type: str) -> str:
        if format_type == "uuid":
            return str(uuid.uuid4())
        charset = CHARSETS.get(format_type, CHARSETS["alphanumeric"])
        return ''.join(random.choice(charset) for _ in range(length))

    @app_commands.command(name="generate-key", description="Generate a single key")
    @app_commands.describe(length="Length of the key", format_type="alphanumeric | hex | numeric | uuid")
    async def generate_key_cmd(self, interaction: discord.Interaction, length: int = 16, format_type: str = "alphanumeric"):
        if format_type != "uuid" and (length < 4 or length > 64):
            await interaction.response.send_message("❌ Length must be between 4 and 64.", ephemeral=True)
            return

        key = self.generate_key(length, format_type)
        await interaction.response.send_message(f"✅ Generated key: `{key}`", ephemeral=BotConfig.EPHEMERAL_RESPONSES)

    @app_commands.command(name="key-batch", description="Generate multiple keys at once")
    @app_commands.describe(count="How many keys (max 20)", length="Length of each key", format_type="alphanumeric | hex | numeric | uuid")
    async def key_batch(self, interaction: discord.Interaction, count: int = 5, length: int = 16, format_type: str = "alphanumeric"):
        if count < 1 or count > 20:
            await interaction.response.send_message("❌ Count must be between 1 and 20.", ephemeral=True)
            return

        keys = [self.generate_key(length, format_type) for _ in range(count)]
        await interaction.response.send_message("✅ Generated keys:\n" + "\n".join(f"`{k}`" for k in keys), ephemeral=BotConfig.EPHEMERAL_RESPONSES)

async def setup(bot: commands.Bot):
    await bot.add_cog(KeyGenerator(bot))
