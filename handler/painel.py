import config
import discord
from handler.entregas import EntregasView
from handler.pingar import PingUserButton
from handler.renomear import RenameChannelButton
import json

# Botão do painel com verificação de cargo
class Painel(discord.ui.Button):
    def __init__(self, allowed_role_id, label="PAINEL STAFF", emoji="🪛", style=discord.ButtonStyle.primary, custom_id="painel_button"):
        super().__init__(label=label, emoji=emoji, style=style, custom_id=custom_id)
        self.allowed_role_id = allowed_role_id  # Armazena o ID do cargo permitido

    async def callback(self, interaction: discord.Interaction):
        # Verifica se o usuário tem o cargo permitido
        if self.allowed_role_id in [role.id for role in interaction.user.roles]:
            embed = discord.Embed(
                title="Painel Staff",
                color=0xff0000
            )

            # Obter o ID do usuário do ticket a partir do arquivo JSON
            ticket_channel_id = interaction.channel.id
            
            user_id = None  # Inicializa a variável aqui

            try:
                with open('tickets.json', 'r') as f:
                    tickets = json.load(f)
                    for ticket in tickets:
                        if ticket['channel_id'] == ticket_channel_id:
                            user_id = ticket['user_id']
                            break
            except FileNotFoundError:
                await interaction.response.send_message(":x: O arquivo de tickets não foi encontrado.", ephemeral=True)
                return

            if user_id:  # Verifica se o user_id foi encontrado
                view = EntregasView()
                view.add_item(PingUserButton(user_id))  # Passando o user_id
                view.add_item(RenameChannelButton(interaction.channel))  # Passando o canal atual

                await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
            else:
                await interaction.response.send_message(":x: Nenhum usuário encontrado para este ticket.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Você não tem permissão para usar este painel.", ephemeral=True)

class PainelView(discord.ui.View):  # Definição da FecharView
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Painel(config.cargo_perm))
