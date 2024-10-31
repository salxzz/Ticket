import discord
from discord.ext import commands
import config
import json

class Entregue(discord.ui.Button):
    def __init__(self, label="DAR CARGO", emoji="💰", style=discord.ButtonStyle.secondary, custom_id="entregue_button"):
        super().__init__(label=label, emoji=emoji, style=style, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        # Verifica se o usuário tem o cargo permitido
        if config.cargo_perm not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("❌ Você não tem permissão para usar este botão.", ephemeral=True)
            return

        # Carregar o ID do canal do ticket
        ticket_channel_id = interaction.channel.id

        # Abrir o JSON com informações dos tickets
        with open('tickets.json', 'r') as f:
            tickets = json.load(f)

        # Encontrar o ticket pelo ID do canal
        ticket_info = next((ticket for ticket in tickets if ticket['channel_id'] == ticket_channel_id), None)

        if ticket_info:
            user_id = ticket_info['user_id']
            guild = interaction.guild
            member = guild.get_member(user_id)

            if member:
                # Verificar se o cargo "cliente" está no config.py
                role = discord.utils.get(guild.roles, id=config.cliente)  # CLIENT_ROLE_ID é o ID do cargo "cliente"

                if role:
                    # Adicionar o cargo ao usuário
                    await member.add_roles(role)
                    await interaction.response.send_message(f"Cargo {role.name} foi dado para {member.name}.", ephemeral=True)
                else:
                    await interaction.response.send_message(":x: Cargo 'cliente' não encontrado!", ephemeral=True)
            else:
                await interaction.response.send_message(":x: Usuário do ticket não encontrado!", ephemeral=True)
        else:
            await interaction.response.send_message(":x: Informações do ticket não encontradas!", ephemeral=True)
