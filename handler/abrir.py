import discord
from discord.ext import commands
import config
import json
from datetime import datetime
from handler.fechar import FecharView
from handler.fechar import Fechar
from handler.fechar import TicketClosedView
from handler.assumir import Assumir
from handler.assumir import AssumirView
from handler.painel import Painel

class EmbedModal(discord.ui.Modal, title="Ticket de Compra"):
    def __init__(self, bot: discord.Client):
        super().__init__()
        self.bot = bot
        self.ModalResposta = discord.ui.TextInput(
            label='Produto Que Deseja Comprar?',
            placeholder='Escreva aqui...',
        )
        self.add_item(self.ModalResposta)

    async def on_submit(self, interaction: discord.Interaction):
        tickets = self.load_tickets()
        user_tickets = [ticket for ticket in tickets if ticket["user_id"] == interaction.user.id and ticket["status"] == "open"]

        if user_tickets:
            await interaction.response.send_message(f"❌ Você já possui um ticket aberto: <#{user_tickets[0]['channel_id']}>", ephemeral=True)
            return

        category = self.bot.get_channel(int(config.category_open))
        channel_name = f'{interaction.user.name.lower()}・ticket'
        new_channel = await category.create_text_channel(name=channel_name)
        mention = interaction.user.mention
        cargo_id = config.cargo_perm
        view = SetarView()

        embed = discord.Embed(
            title="Ticket de Compra",
            color=discord.Color.from_rgb(255, 215, 0)
        )
        embed.add_field(name="📝 | Ticket criado por:", value=mention, inline=False)
        embed.add_field(name="🪪 | ID do Canal:", value=new_channel.id, inline=False)  # Usando o ID do canal
        embed.add_field(name="👑 | Ticket assumido por:", value="Não foi assumido", inline=False)
        embed.add_field(name="🛒 | Produto:", value=f"```{self.ModalResposta.value}```", inline=False)  # Corrigido para .value
        embed.set_footer(text=f"Criado por: {interaction.user}", icon_url=interaction.user.avatar.url)

        await new_channel.send(f"{mention} - <@&{cargo_id}>", embed=embed, view=view)
        await new_channel.set_permissions(interaction.user, read_messages=True, send_messages=True, attach_files=True)

        # Salvar informações do ticket, incluindo o status de "assumido" como "Não foi assumido"
        self.save_ticket_info(interaction.user, new_channel.id, "open", assumed=False)
        await interaction.response.send_message(f"✔ *Ticket Criado {new_channel.mention}*", ephemeral=True)

        # Enviar mensagem de log no canal de logs
        await self.send_log(interaction, new_channel, assumed=False)  # Passando o status de assumido

    def save_ticket_info(self, user, channel_id, status, assumed):
        ticket_info = {
            "user_id": user.id,
            "user_name": str(user),
            "channel_id": channel_id,
            "channel_name": f"{user.name.lower()}・ticket",
            "product": self.ModalResposta.value,
            "status": status,
            "assumed": user.id if assumed else "Não foi assumido",  # Armazena o ID do usuário que assumiu o ticket ou "Não foi assumido"
            "created_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }

        try:
            with open("tickets.json", "r") as file:
                tickets = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            tickets = []

        tickets.append(ticket_info)

        with open("tickets.json", "w") as file:
            json.dump(tickets, file, indent=4)

    def load_tickets(self):
        try:
            with open("tickets.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    async def send_log(self, interaction: discord.Interaction, new_channel, assumed):
        """Função para enviar logs quando um ticket é criado"""
        logs_channel = self.bot.get_channel(int(config.logs))
        if logs_channel:
            log_embed = discord.Embed(
                title="🎟️ Novo Ticket Criado",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )

            # Adicionando informações como fields na embed
            log_embed.add_field(name="👥 Usuário:", value=interaction.user.mention, inline=True)
            log_embed.add_field(name="📍 Canal:", value=new_channel.mention, inline=True)
            log_embed.add_field(name="🛒 Produto:", value=self.ModalResposta.value, inline=False)
            log_embed.add_field(name="⏰️ Data de Criação:", value=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), inline=True)
            log_embed.add_field(name="👑 Assumido:", value="Não foi assumido", inline=False)  # Incluindo o status de assumido no log
            log_embed.set_footer(text=f"ID do Usuário: {interaction.user.id}")

            await logs_channel.send(embed=log_embed)

class Abrir(discord.ui.Button):
    def __init__(self, label="COMPRAR", emoji="🛒", style=discord.ButtonStyle.primary, custom_id="abrir_button"):
        super().__init__(label=label, emoji=emoji, style=style, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        modal = EmbedModal(bot=interaction.client)  
        await interaction.response.send_modal(modal)

class AbrirView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Abrir())

class SetarView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Fechar())  
        self.add_item(Assumir())
        self.add_item(Painel(config.cargo_perm))
