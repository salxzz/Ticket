import discord
import config  # Certifique-se de que o arquivo config.py está no mesmo diretório ou no caminho correto.

# Botão para enviar a embed ao canal de entregas
class EnviarEmbed(discord.ui.Button):
    def __init__(self):
        super().__init__(label="POSTAR", emoji="📦", style=discord.ButtonStyle.secondary, custom_id="enviar_embed_button")

    async def callback(self, interaction: discord.Interaction):
        # Obtém a embed da mensagem atual
        embed = interaction.message.embeds[0] if interaction.message.embeds else None
        
        if embed:
            # Obtém o canal de entregas a partir da configuração
            canal_entregas = interaction.client.get_channel(int(config.entregas))
            if canal_entregas:
                await canal_entregas.send(embed=embed)
                await interaction.response.send_message("✅ entrega enviada!", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Erro ao enviar a embed. Canal não encontrado.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Nenhuma embed encontrada na mensagem.", ephemeral=True)

