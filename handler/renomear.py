import discord
from discord.ui import Button, Modal, TextInput
import json

# Botão para renomear o canal
class RenameChannelButton(discord.ui.Button):
    def __init__(self, channel, custom_id="rename_channel_button"):
        super().__init__(label="RENOMEAR",emoji='✏️', style=discord.ButtonStyle.secondary, custom_id=custom_id)
        self.channel = channel  # Armazena a referência do canal

    async def callback(self, interaction: discord.Interaction):
        # Abre o modal para renomear o canal
        modal = RenameChannelModal(self.channel)
        await interaction.response.send_modal(modal)

# Modal para renomear o canal
class RenameChannelModal(Modal):
    def __init__(self, channel):
        super().__init__(title="Renomear Canal")
        self.channel = channel  # Recebe o canal que será renomeado
        self.new_name = TextInput(
            label='Novo Nome do Canal',
            placeholder='Digite o novo nome do canal...',
            required=True  # Torna obrigatório o preenchimento do campo
        )
        self.add_item(self.new_name)

    async def on_submit(self, interaction: discord.Interaction):
        new_channel_name = self.new_name.value
        
        # Renomeia o canal
        await self.channel.edit(name=new_channel_name)
        
        # Atualiza o tickets.json com o novo nome do canal
        try:
            with open('tickets.json', 'r') as f:
                tickets = json.load(f)

            for ticket in tickets:
                if ticket['channel_id'] == self.channel.id:
                    ticket['channel_name'] = new_channel_name  # Atualiza o nome do canal
                    break

            with open('tickets.json', 'w') as f:
                json.dump(tickets, f, indent=4)

            await interaction.response.send_message(f"✅ Canal renomeado para **{new_channel_name}** com sucesso!", ephemeral=True)
        except FileNotFoundError:
            await interaction.response.send_message(":x: O arquivo de tickets não foi encontrado.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f":x: Ocorreu um erro ao atualizar o nome do canal: {e}", ephemeral=True)
