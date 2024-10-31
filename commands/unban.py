import discord
from discord.ext import commands

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member_id: int, *, reason=None):
        try:
            user = await self.bot.fetch_user(member_id)
            await ctx.guild.unban(user, reason=reason)
            embed = discord.Embed(title=f":white_check_mark: {user.name} foi desbanido com sucesso!")
            if reason:
                embed.add_field(name="Razão", value=reason, inline=True)
            await ctx.send(embed=embed)
        except discord.NotFound:
            await ctx.send(":x: Usuário não encontrado!")
        except Exception as e:
            await ctx.send(f":x: Ocorreu um erro ao tentar desbanir o membro: {e}")

async def setup(bot):
    await bot.add_cog(Unban(bot))
