import discord
from discord.ext import commands
import config  # Assegure-se de que o config.py está no mesmo diretório

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: str = None, *, reason: str = None):
        if member is None:
            await ctx.send(f":x: Você precisa fornecer um membro para banir. Use: `.ban <membro> [razão]`")
            return
        
        try:
            # Inicializa a variável user para uso posterior
            user = None

            # Tenta encontrar o membro pelo ID fornecido
            if member.isdigit():  # Verifica se o argumento é um ID
                user_id = int(member)
                user = await self.bot.fetch_user(user_id)  # Obtém o usuário
                await ctx.guild.ban(user, reason=reason)  # Bane o usuário
                embed = discord.Embed(
                    title=":white_check_mark: Membro banido!",
                    description=f"{user.name} foi banido do servidor.",
                    color=0x00ff00
                )
            else:
                # Se não for um ID, tenta encontrar o membro pelo nome
                member = await commands.MemberConverter().convert(ctx, member)
                await ctx.guild.ban(member, reason=reason)  # Bane o membro
                user = member  # Define user como o membro banido
                embed = discord.Embed(
                    title=":white_check_mark: Membro banido!",
                    description=f"{member.name} foi banido do servidor.",
                    color=0x00ff00
                )

            if reason:
                embed.add_field(name="Razão", value=reason, inline=True)  # Adiciona razão se fornecida

            await ctx.send(embed=embed)

            # Enviando log para o canal de logs
            logs_channel = self.bot.get_channel(config.logs)
            if logs_channel:
                log_embed = discord.Embed(
                    title=":white_check_mark: Membro Banido",
                    description=f"{user.name} foi banido do servidor.",
                    color=0x00ff00
                )
                if reason:
                    log_embed.add_field(name="Razão", value=reason, inline=True)
                log_embed.add_field(name="Comando usado por", value=ctx.author.mention, inline=True)
                await logs_channel.send(embed=log_embed)
            else:
                await ctx.send(":x: Canal de logs não encontrado!")

        except discord.NotFound:
            await ctx.send(":x: Usuário não encontrado. Verifique o ID e tente novamente.")
        except commands.MemberNotFound:
            await ctx.send(":x: Membro não encontrado. Verifique o nome e tente novamente.")
        except Exception as e:
            await ctx.send(f":x: Ocorreu um erro ao tentar banir o membro: {str(e)}")

async def setup(bot):
    await bot.add_cog(Ban(bot))
