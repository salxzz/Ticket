import discord
from discord.ext import commands

class SlashPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @discord.app_commands.command(name="ping", description="[📶] Responde com Pong!")
    async def ping(self, interaction: discord.Interaction):
        latency = self.bot.latency * 1000
        await interaction.response.send_message(f'🏓 Pong! {latency:.2f} ms', ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(SlashPing(bot))
