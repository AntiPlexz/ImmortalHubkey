import discord
from discord import app_commands
from discord.ext import commands
from config import BotConfig

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="key-help", description="Show help for ImmortalHubKey")
    async def key_help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="ImmortalHubKey – Commands",
            color=discord.Color.blurple()
        )
        embed.add_field(name="/generate-key", value="Generate a single key", inline=False)
        embed.add_field(name="/key-batch", value="Generate multiple keys", inline=False)
        embed.add_field(name="/key-help", value="Show this help message", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=BotConfig.EPHEMERAL_RESPONSES)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))
