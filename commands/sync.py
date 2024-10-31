from discord.ext import commands

class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx: commands.Context):
        if ctx.author.id == 1149804841162518540:  
            sincs = await self.bot.tree.sync() 
            await ctx.message.delete()
            await ctx.send(f"({len(sincs)}) comandos sincronizados", delete_after=5)
        else:
            await ctx.reply('Apenas o meu dono pode usar esse comando!', delete_after=3)

async def setup(bot):
    await bot.add_cog(Sync(bot))
