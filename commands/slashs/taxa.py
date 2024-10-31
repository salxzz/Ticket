import discord
from discord.ext import commands
import math

# Define os valores em reais para Robux sem e com taxa
VALOR_ROBUX_SEM_TAXA = 27.00  # R$27,00 para 1000 Robux sem taxa
VALOR_ROBUX_COM_TAXA = 35.00  # R$35,00 para 1429 Robux com taxa (incluindo os 30%)

class TaxaCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @discord.app_commands.command(name="taxa", description="[🏷] Calcula a taxa do roblox e o valor em reais.")
    async def taxa(self, interaction: discord.Interaction, robux: int):
        # Calcula o valor necessário para que o cliente receba o Robux solicitado após a taxa de 30%
        robux_com_taxa = math.ceil(robux / 0.70)  # Divide por 0.70 para compensar a taxa de 30%

        # Calcula o valor em reais baseado nos valores fixos
        valor_sem_taxa_reais = VALOR_ROBUX_SEM_TAXA * (robux / 1000)  # Proporcional ao valor base sem taxa
        valor_com_taxa_reais = VALOR_ROBUX_COM_TAXA * (robux_com_taxa / 1429)  # Proporcional ao valor base com taxa

        # Cria uma embed com a informação
        embed = discord.Embed(
            title="💸 Cálculo de Taxa de Robux 💸",
            color=discord.Color.from_rgb(255, 255, 255)  # Cor branca
        )
        
        embed.add_field(
            name="📥 Robux Original:",
            value=f"{int(robux)} Robux = R$ {valor_sem_taxa_reais:.2f}",
            inline=False
        )
        
        embed.add_field(
            name="📤 Robux com Taxa:",
            value=f"{robux_com_taxa} Robux = R$ {valor_com_taxa_reais:.2f}",
            inline=False
        )
        
        embed.set_thumbnail(url=interaction.client.user.avatar.url)  # Colocando a foto de perfil do bot
        
        await interaction.response.send_message(embed=embed)

# Função para configurar o cog
async def setup(bot):
    await bot.add_cog(TaxaCommand(bot))
