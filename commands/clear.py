import discord
from discord.ext import commands

class ClearCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        if amount < 2 or amount > 1000:
            await ctx.send("Por favor, insira um número entre 2 e 1000.", delete_after=5)  # Mensagem temporária
            return
        
        deleted = await ctx.channel.purge(limit=amount + 1, check=lambda m: not m.pinned)  # Ignora mensagens fixadas

        # Verifica se há mensagens deletadas
        if len(deleted) > 1:
            await ctx.send(f'{ctx.author.mention}, {len(deleted) - 1} mensagens foram deletadas.', delete_after=5)  # Mensagem temporária
        else:
            await ctx.send(f'{ctx.author.mention}, não havia mensagens para deletar.', delete_after=5)  # Mensagem temporária

async def setup(bot):
    await bot.add_cog(ClearCommand(bot))
