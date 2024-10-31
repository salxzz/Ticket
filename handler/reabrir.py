import discord
from discord.ext import commands
import config
import json
from datetime import datetime

class Reabrir(discord.ui.Button):
    def __init__(self, label="ABRIR", emoji="🔓", style=discord.ButtonStyle.green, custom_id="reabrir_button"):
        super().__init__(label=label, emoji=emoji, style=style, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        # Carregar tickets existentes
        tickets = self.load_tickets()

        # Encontrar o ticket correspondente ao canal atual
        current_channel = interaction.channel
        ticket = next((ticket for ticket in tickets if ticket["channel_id"] == current_channel.id and ticket["status"] == "closed"), None)

        if not ticket:
            await interaction.response.send_message("❌ Este canal não é um ticket fechado ou já foi reaberto.", ephemeral=True)
            return

        # Mover o canal de volta para a categoria de tickets abertos
        open_category = interaction.client.get_channel(int(config.category_open))
        await current_channel.edit(category=open_category)

        # Conceder as permissões ao usuário para o canal
        user = interaction.guild.get_member(ticket["user_id"])
        if user:
            await current_channel.set_permissions(user, read_messages=True, send_messages=True, attach_files=True)

        # Atualizar o status do ticket para "open"
        ticket["status"] = "open"
        self.save_tickets(tickets)

        # Enviar uma mensagem de confirmação no canal e como resposta
        await current_channel.send(f"🔓 Ticket reaberto por {interaction.user.mention}.")
        await interaction.response.send_message("✔ Ticket reaberto com sucesso.", ephemeral=True)

        # Remover a mensagem do botão
        await interaction.message.delete()

    def load_tickets(self):
        """Carrega a lista de tickets a partir do arquivo tickets.json"""
        try:
            with open("tickets.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tickets(self, tickets):
        """Salva a lista de tickets atualizada no arquivo tickets.json"""
        with open("tickets.json", "w") as file:
            json.dump(tickets, file, indent=4)

class ReabrirView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Reabrir())  # Corrigido para usar o botão Reabrir
