import discord
from discord.ext import commands
import config
import json
from datetime import datetime
from handler.assumir import Assumir
from handler.assumir import AssumirView
from handler.reabrir import Reabrir
from handler.excluir import Excluir
from handler.entregue import Entregue


class Fechar(discord.ui.Button):
    def __init__(self, label="FECHAR", emoji="🔒", style=discord.ButtonStyle.red, custom_id="fechar_button"):
        super().__init__(label=label, emoji=emoji, style=style, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        # Verifica se o usuário tem o cargo permitido
        if config.cargo_perm not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("Você não tem permissão para fechar este ticket.", ephemeral=True)
            return

        tickets = self.load_tickets()
        current_channel = interaction.channel
        ticket = next((ticket for ticket in tickets if ticket["channel_id"] == current_channel.id and ticket["status"] == "open"), None)

        if not ticket:
            await interaction.response.send_message("❌ Este canal não é um ticket aberto ou já foi fechado.", ephemeral=True)
            return

        closed_category = interaction.client.get_channel(int(config.category_closed))
        await current_channel.edit(category=closed_category)
        user = interaction.guild.get_member(ticket["user_id"])
        if user:
            await current_channel.set_permissions(user, overwrite=None)

        ticket["status"] = "closed"
        self.save_tickets(tickets)

        await self.send_log(interaction, ticket, interaction.user)

        view = TicketClosedView()
        await current_channel.send(f"🚫 Ticket fechado por {interaction.user.mention}.", view=view)
        await interaction.response.send_message("✔ Ticket fechado com sucesso.", ephemeral=True)

    async def send_log(self, interaction: discord.Interaction, ticket, closed_by):
        logs_channel = interaction.client.get_channel(int(config.logs))
        if logs_channel:
            log_embed = discord.Embed(
                title="🎟️ Ticket Fechado",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            log_embed.add_field(name="👥 Usuário:", value=closed_by.mention, inline=True)
            log_embed.add_field(name="📍 Canal:", value=f"<#{ticket['channel_id']}>", inline=True)
            log_embed.add_field(name="👑 Assumido Por:", value=ticket.get("assumed_by", "Não foi assumido"), inline=False)
            log_embed.add_field(name="⏰️ Data de Fechamento:", value=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), inline=True)
            log_embed.set_footer(text=f"ID do Usuário: {closed_by.id}")

            await logs_channel.send(embed=log_embed)

    def load_tickets(self):
        try:
            with open("tickets.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tickets(self, tickets):
        with open("tickets.json", "w") as file:
            json.dump(tickets, file, indent=4)

class TicketClosedView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Reabrir())  # Botão para reabrir o ticket
        self.add_item(Excluir())  # View para excluir
        self.add_item(Entregue())


class FecharView(discord.ui.View):  # Definição da FecharView
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Fechar())
