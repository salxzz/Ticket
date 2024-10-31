import discord
from discord.ext import commands
from datetime import timedelta

class MuteSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="mute", description="[🔇] Muta um membro por um tempo específico.")
    @discord.app_commands.checks.has_permissions(kick_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, time: str, reason: str = None):
        if interaction.user.id == member.id:
            await interaction.response.send_message(":x: Você não pode se mutar!", ephemeral=True)
            return

        # Variável para armazenar o valor formatado do tempo
        duration = None  

        # Definindo o timeout baseado no tempo fornecido
        if "m" in time:
            time_value = time.replace("m", "")
            duration = timedelta(minutes=int(time_value))
            duration_str = f"{time_value} minutos"
        elif "h" in time:
            time_value = time.replace("h", "")
            duration = timedelta(hours=int(time_value))
            duration_str = f"{time_value} horas"
        elif "d" in time:
            time_value = time.replace("d", "")
            duration = timedelta(days=int(time_value))
            duration_str = f"{time_value} dias"
        else:
            await interaction.response.send_message(":x: Formato de tempo inválido! Use 'm' para minutos, 'h' para horas, ou 'd' para dias.", ephemeral=True)
            return

        # Aplicando o timeout
        try:
            await member.edit(timed_out_until=discord.utils.utcnow() + duration, reason=reason)
        except Exception as e:
            await interaction.response.send_message(f":x: Ocorreu um erro ao tentar mutar o membro: {e}", ephemeral=True)
            return

        # Criação da embed com o tempo e a razão (se fornecida)
        embed = discord.Embed(title=f":white_check_mark: {member.name} foi mutado com sucesso!")
        embed.add_field(name="Duração", value=duration_str, inline=True)

        if reason:
            embed.add_field(name="Razão", value=reason, inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(MuteSlash(bot))
