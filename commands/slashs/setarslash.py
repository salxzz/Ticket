import discord
from discord.ext import commands
from discord import app_commands
from handler.abrir import AbrirView
from handler.fechar import Fechar
from handler.fechar import TicketClosedView
from handler.assumir import Assumir
from handler.fechar import FecharView
from handler.assumir import AssumirView
from handler.painel import PainelView
import config

class SetarSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setar", description="[🛒] Envia o painel de compras.")
    @app_commands.checks.has_permissions(manage_channels=True)  # Troque isso para a verificação do seu cargo específico
    async def setar(self, interaction: discord.Interaction):
        view = AbrirView()
        embed = discord.Embed(
            title="⭐️Painel de compras⭐️",
            color=0xff0000,
            description="-  **Tickets apenas para compras. **🛒\n\n_**Seja claro com o que deseja comprar, não tome tempo desnecessário da administração**_"
        )
        embed.add_field(name="Produtos:", value="https://discord.com/channels/1263180349198827532/1263210505980350475\n"
                                                "https://discord.com/channels/1263180349198827532/1263210533230739466\n"
                                                "https://discord.com/channels/1263180349198827532/1263887045198348410\n"
                                                "https://discord.com/channels/1263180349198827532/1263887219026821272\n"
                                                "https://discord.com/channels/1263180349198827532/1263207110594789378\n"
                                                "https://discord.com/channels/1263180349198827532/1263207862541484165\n"
                                                "https://discord.com/channels/1263180349198827532/1263208281913036901\n"
                                                "https://discord.com/channels/1263180349198827532/1263209184258953259",
                        inline=False)
        
        await interaction.response.send_message("Painel de compras enviado com sucesso!", ephemeral=True)
        await interaction.channel.send(embed=embed, view=view)


async def setup(bot):
    bot.add_view(AbrirView())
    bot.add_view(FecharView())
    bot.add_view(TicketClosedView())
    bot.add_view(AssumirView())
    bot.add_view(PainelView())
    await bot.add_cog(SetarSlash(bot))
