import discord
import json
import config
from discord.utils import get

class Assumir(discord.ui.Button):
    def __init__(self, label="ASSUMIR", emoji="👑", style=discord.ButtonStyle.green, custom_id="assumir_button"):
        super().__init__(label=label, emoji=emoji, style=style, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        user_roles = interaction.user.roles
        necessary_role = get(user_roles, id=config.cargo_perm)

        if necessary_role is not None:
            # Acessar o embed da mensagem
            if not interaction.message.embeds:
                await interaction.response.send_message("❌ Não há informações de ticket nesta mensagem.", ephemeral=True)
                return

            embed = interaction.message.embeds[0]
            assumido_por = next((field for field in embed.fields if field.name == "👑 | Ticket assumido por:"), None)

            # Atualizar o embed
            if assumido_por:
                embed.remove_field(embed.fields.index(assumido_por))

            embed.insert_field_at(2, name="👑 | Ticket assumido por:", value=interaction.user.mention, inline=False)
            await interaction.response.edit_message(embed=embed)

            # Atualizar o nome do canal
            new_channel_name = f"✅ {interaction.channel.name}"
            await interaction.channel.edit(name=new_channel_name)

            # Atualizar o arquivo JSON
            self.update_ticket_info(interaction.channel.id, interaction.user.id)

            # Mensagem de confirmação
            await interaction.followup.send(f"✔️ Ticket assumido por {interaction.user.mention}.", ephemeral=True)

        else:
            await interaction.response.send_message("🚫 Você não tem permissão para assumir este ticket.", ephemeral=True)

    def update_ticket_info(self, channel_id, user_id):
        """Atualiza o arquivo JSON com as informações do ticket assumido."""
        tickets = self.load_tickets()
        ticket = next((ticket for ticket in tickets if ticket["channel_id"] == channel_id), None)

        if ticket:
            ticket["assumed"] = "Sim"
            ticket["assumed_by"] = user_id  # Armazena o ID do usuário que assumiu o ticket
            self.save_tickets(tickets)

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

class AssumirView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Assumir())
