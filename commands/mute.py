import discord
from discord.ext import commands
from datetime import timedelta
import config  # Assegure-se de que o config.py está no mesmo diretório

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member = None, time: str = None, *, reason=None):
        if member is None:
            await ctx.send(":x: Você precisa mencionar um membro para mutar. Use: `.mute <membro> <tempo> [razão]`")
            return

        if time is None:
            await ctx.send(":x: Você precisa especificar um tempo para o mute (ex: 10m, 1h, 2d).")
            return

        if ctx.author.id == member.id:
            await ctx.channel.send(":x: Você não pode se mutar!")
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
            await ctx.channel.send(":x: Formato de tempo inválido! Use 'm' para minutos, 'h' para horas, ou 'd' para dias.")
            return

        # Aplicando o timeout
        try:
            await member.edit(timed_out_until=discord.utils.utcnow() + duration, reason=reason)
        except Exception as e:
            await ctx.channel.send(f":x: Ocorreu um erro ao tentar mutar o membro: {e}")
            return

        # Criação da embed com o tempo e a razão (se fornecida)
        embed = discord.Embed(title=f":white_check_mark: {member.name} foi mutado com sucesso!")
        embed.add_field(name="Duração", value=duration_str, inline=True)

        if reason:
            embed.add_field(name="Razão", value=reason, inline=True)

        await ctx.send(embed=embed)

        # Enviando a embed para o canal de logs
        logs_channel = self.bot.get_channel(config.logs)  # Acesse o canal de logs pelo ID definido em config
        if logs_channel:
            log_embed = discord.Embed(title=f":white_check_mark: Membro Mutado")
            log_embed.add_field(name="Membro", value=member.mention, inline=True)
            log_embed.add_field(name="Duração", value=duration_str, inline=True)
            log_embed.add_field(name="Comando usado por", value=ctx.author.mention, inline=True)

            if reason:
                log_embed.add_field(name="Razão", value=reason, inline=True)

            await logs_channel.send(embed=log_embed)
        else:
            await ctx.send(":x: Canal de logs não encontrado!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):
        if ctx.author.id == member.id:
            await ctx.channel.send(":x: Você não pode se desmutar!")
            return

        # Removendo o timeout
        try:
            await member.edit(timed_out_until=None)
        except Exception as e:
            await ctx.channel.send(f":x: Ocorreu um erro ao tentar desmutar o membro: {e}")
            return

        # Criação da embed confirmando que o membro foi desmutado
        embed = discord.Embed(title=f":white_check_mark: {member.name} foi desmutado com sucesso!")
        await ctx.send(embed=embed)

        # Enviando a embed para o canal de logs
        logs_channel = self.bot.get_channel(config.logs)
        if logs_channel:
            log_embed = discord.Embed(title=f":white_check_mark: Membro Desmutado")
            log_embed.add_field(name="Membro", value=member.mention, inline=True)
            log_embed.add_field(name="Comando usado por", value=ctx.author.mention, inline=True)

            await logs_channel.send(embed=log_embed)
        else:
            await ctx.send(":x: Canal de logs não encontrado!")

async def setup(bot):
    await bot.add_cog(Mute(bot))
