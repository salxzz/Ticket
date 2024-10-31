import discord
from discord import app_commands
from discord.ext import commands
import config

class InfosBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(description='Informações do bot')
    async def info(self, interaction: discord.Interaction):
        # Verifica se o usuário tem o cargo permitido
        if config.cargo_perm not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)
            return
        
        # Obtém a URL da foto de perfil do bot
        bot_avatar_url = self.bot.user.avatar.url

        # Obtém o servidor e ping
        server_name = interaction.guild.name
        server_id = interaction.guild.id
        bot_ping = round(self.bot.latency * 1000)  # Latência em milissegundos

        # Criação da embed com informações do config.py
        embed = discord.Embed(
            description="**Informações sobre o bot**",
            color=discord.Color.from_rgb(255, 255, 255)
        )

        # Adiciona os campos na embed com inline=True
        embed.add_field(name="🛠 Dono do Bot:", value="<@1149804841162518540>", inline=True)
        embed.add_field(name="📋 Servidor:", value=f"{server_name} (ID: {server_id})", inline=True)
        embed.add_field(name="📶 Ping:", value=f"{bot_ping} ms", inline=True)
        embed.add_field(name="🤖 Versão do Bot:", value="V4.0", inline=True)
        
        # Define a miniatura da embed com a foto de perfil do bot
        embed.set_thumbnail(url=bot_avatar_url)
        
        # Envia a embed para o canal onde o comando foi chamado
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(InfosBot(bot))
