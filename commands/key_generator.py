"""
Key Generator Commands for ImmortalHubKey
"""

import discord
from discord.ext import commands
from discord import app_commands
import logging
from utils.key_utils import KeyGenerator
from config import BotConfig

logger = logging.getLogger(__name__)

class KeyGeneratorCog(commands.Cog):
    """Cog containing key generation commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.key_generator = KeyGenerator()
        self.EPHEMERAL = BotConfig.EPHEMERAL_RESPONSES
    
    @app_commands.command(name="generate-key", description="Generate a random key")
    async def generate_key(self, interaction: discord.Interaction, length: int = 16, format_type: str = "alphanumeric"):
        try:
            if length < BotConfig.MIN_KEY_LENGTH or length > BotConfig.MAX_KEY_LENGTH:
                await interaction.response.send_message(
                    f"❌ Key length must be {BotConfig.MIN_KEY_LENGTH}-{BotConfig.MAX_KEY_LENGTH}.",
                    ephemeral=self.EPHEMERAL
                )
                return
            
            valid_formats = ["alphanumeric", "hex", "uuid"]
            if format_type.lower() not in valid_formats:
                await interaction.response.send_message(
                    f"❌ Invalid format. Use one of: {', '.join(valid_formats)}",
                    ephemeral=self.EPHEMERAL
                )
                return
            
            if format_type.lower() == "uuid":
                key = self.key_generator.generate_uuid()
                key_info = "UUID (36 chars)"
            elif format_type.lower() == "hex":
                key = self.key_generator.generate_hex_key(length)
                key_info = f"Hex ({length} chars)"
            else:
                key = self.key_generator.generate_alphanumeric_key(length)
                key_info = f"Alphanumeric ({length} chars)"
            
            embed = discord.Embed(title="🔑 ImmortalHubKey Generated Key", color=discord.Color.green())
            embed.add_field(name="Key", value=f"`{key}`", inline=False)
            embed.add_field(name="Format", value=key_info, inline=True)
            embed.add_field(name="Requested by", value=interaction.user.mention, inline=True)
            embed.set_footer(text="⚠️ Keep your key secure!")
            
            await interaction.response.send_message(embed=embed, ephemeral=self.EPHEMERAL)
            logger.info(f"Generated {format_type} key for {interaction.user} (ID {interaction.user.id})")
        except Exception as e:
            logger.error(f"Error generating key: {e}")
            await interaction.response.send_message("❌ Error generating key.", ephemeral=self.EPHEMERAL)
    
    @app_commands.command(name="key-batch", description="Generate multiple keys")
    async def generate_key_batch(self, interaction: discord.Interaction, count: int, length: int = 16, format_type: str = "alphanumeric"):
        try:
            if count < 1 or count > BotConfig.MAX_BATCH_SIZE:
                await interaction.response.send_message(
                    f"❌ Count must be 1-{BotConfig.MAX_BATCH_SIZE}.",
                    ephemeral=self.EPHEMERAL
                )
                return
            if length < BotConfig.MIN_KEY_LENGTH or length > BotConfig.MAX_KEY_LENGTH:
                await interaction.response.send_message(
                    f"❌ Length must be {BotConfig.MIN_KEY_LENGTH}-{BotConfig.MAX_KEY_LENGTH}.",
                    ephemeral=self.EPHEMERAL
                )
                return
            
            valid_formats = ["alphanumeric", "hex", "uuid"]
            if format_type.lower() not in valid_formats:
                await interaction.response.send_message(
                    f"❌ Invalid format. Use one of: {', '.join(valid_formats)}",
                    ephemeral=self.EPHEMERAL
                )
                return
            
            keys = []
            for _ in range(count):
                if format_type.lower() == "uuid":
                    keys.append(self.key_generator.generate_uuid())
                elif format_type.lower() == "hex":
                    keys.append(self.key_generator.generate_hex_key(length))
                else:
                    keys.append(self.key_generator.generate_alphanumeric_key(length))
            
            embed = discord.Embed(title=f"🔑 ImmortalHubKey Generated {count} Keys", color=discord.Color.blue())
            key_text = "\n".join([f"`{k}`" for k in keys])
            if len(key_text) > 1024:
                for i in range(0, len(keys), 5):
                    batch = keys[i:i+5]
                    embed.add_field(name=f"Keys {i+1}-{min(i+5, len(keys))}", value="\n".join([f"`{k}`" for k in batch]), inline=False)
            else:
                embed.add_field(name="Keys", value=key_text, inline=False)
            
            embed.add_field(name="Format", value=f"{format_type.title()}", inline=True)
            embed.add_field(name="Requested by", value=interaction.user.mention, inline=True)
            embed.set_footer(text="⚠️ Keep your keys secure!")
            
            await interaction.response.send_message(embed=embed, ephemeral=self.EPHEMERAL)
        except Exception as e:
            logger.error(f"Error generating key batch: {e}")
            await interaction.response.send_message("❌ Error generating keys.", ephemeral=self.EPHEMERAL)
    
    @app_commands.command(name="ping", description="Check ImmortalHubKey bot latency")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"🏓 Pong! {round(self.bot.latency*1000)}ms", ephemeral=self.EPHEMERAL)
    
    @app_commands.command(name="key-help", description="Help with ImmortalHubKey commands")
    async def key_help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🔑 ImmortalHubKey Help", color=discord.Color.gold())
        embed.add_field(name="/generate-key", value="Generate a single key", inline=False)
        embed.add_field(name="/key-batch", value="Generate multiple keys", inline=False)
        embed.add_field(name="/ping", value="Check bot latency", inline=False)
        embed.set_footer(text="Commands are slash-only. Keys are sent as ephemeral.")
        await interaction.response.send_message(embed=embed, ephemeral=self.EPHEMERAL)
