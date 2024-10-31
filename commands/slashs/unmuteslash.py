import discord
from discord.ext import commands

class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="unmute", description="[🔊] Desmuta um membro.")
    @discord.app_commands.checks.has_permissions(kick_members=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        if interaction.user.id == member.id:
            await interaction.response.send_message(":x: Você não pode se desmutar!", ephemeral=True)
            return

        # Removendo o timeout
        try:
            await member.edit(timed_out_until=None)
        except Exception as e:
            await interaction.response.send_message(f":x: Ocorreu um erro ao tentar desmutar o membro: {e}", ephemeral=True)
            return

        # Criação da embed confirmando que o membro foi desmutado
        embed = discord.Embed(title=f":white_check_mark: {member.name} foi desmutado com sucesso!")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Unmute(bot))
