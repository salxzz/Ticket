import discord
from discord.ext import commands
from handler.abrir import AbrirView
from handler.fechar import Fechar
from handler.fechar import TicketClosedView
from handler.assumir import Assumir
from handler.fechar import FecharView
from handler.assumir import AssumirView
from handler.painel import PainelView
import config

class Setar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setar(self, ctx):
        # Verifica se o usuário tem o cargo de permissão
        if config.cargo_perm in [role.id for role in ctx.author.roles]:
            view = AbrirView()
            embed = discord.Embed(
                title="⭐️Painel de compras⭐️",
                colour=0xff0000,
                description="-  **Tickets apenas para compras. **🛒\n\n_**Seja claro com o que deseja comprar, não tome tempo desnecessário da administração**_"
            )
            embed.add_field(name="Produtos:", value="https://discord.com/channels/1263180349198827532/1263210505980350475\nhttps://discord.com/channels/1263180349198827532/1263210533230739466\nhttps://discord.com/channels/1263180349198827532/1263887045198348410\nhttps://discord.com/channels/1263180349198827532/1263887219026821272\nhttps://discord.com/channels/1263180349198827532/1263207110594789378\nhttps://discord.com/channels/1263180349198827532/1263207862541484165\nhttps://discord.com/channels/1263180349198827532/1263208281913036901\nhttps://discord.com/channels/1263180349198827532/1263209184258953259", inline=False)
            await ctx.send(embed=embed, view=view)
        else:
            await ctx.send("Você não tem permissão para usar este comando.")

async def setup(bot):
    bot.add_view(AbrirView())
    bot.add_view(FecharView())
    bot.add_view(TicketClosedView())
    bot.add_view(AssumirView())
    bot.add_view(PainelView())
    await bot.add_cog(Setar(bot))
