import discord
from discord.ext import commands
from discord import app_commands

class BanSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="[🚫] Bane um membro do servidor.")
    @app_commands.describe(member="Membro a ser banido", reason="Razão do banimento")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if interaction.user.id == member.id:
            await interaction.response.send_message(":x: Você não pode se banir!", ephemeral=True)
            return

        try:
            await member.ban(reason=reason)
            embed = discord.Embed(title=":white_check_mark: Membro banido!", description=f"{member.name} foi banido do servidor.", color=0xff0000)
            if reason:
                embed.add_field(name="Razão", value=reason, inline=True)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f":x: Ocorreu um erro ao tentar banir o membro: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(BanSlash(bot))
