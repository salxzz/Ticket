import discord
from discord.ext import commands
import json
import asyncio
import config

class DeleteTicket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="delete_ticket", description="[🪛] Deleta as informações do ticket atual e o canal.")
    async def delete_ticket(self, interaction: discord.Interaction):
        # Verifica se o usuário tem o cargo de permissão
        if config.cargo_perm not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message(":x: Apenas usuários com o cargo apropriado podem usar esse comando.", ephemeral=True)
            return

        # Identificar o canal atual do ticket
        ticket_channel_id = interaction.channel.id

        # Carregar o arquivo JSON com as informações dos tickets
        try:
            with open('tickets.json', 'r') as f:
                tickets = json.load(f)
        except FileNotFoundError:
            await interaction.response.send_message(":x: O arquivo de tickets não foi encontrado.", ephemeral=True)
            return

        # Verificar se o ticket existe no arquivo
        ticket_exists = False
        updated_tickets = [ticket for ticket in tickets if ticket['channel_id'] != ticket_channel_id]

        if len(updated_tickets) < len(tickets):
            ticket_exists = True

        # Se o ticket foi encontrado e removido, salvar as mudanças no JSON
        if ticket_exists:
            with open('tickets.json', 'w') as f:
                json.dump(updated_tickets, f, indent=4)

            # Mensagem de confirmação e apagar canal
            await interaction.response.send_message(f":white_check_mark: O ticket do canal {interaction.channel.name} foi deletado. O canal será removido em 3 segundos.", ephemeral=True)

            # Espera 3 segundos antes de apagar o canal
            await asyncio.sleep(3)
            await interaction.channel.delete(reason="Ticket deletado")
        else:
            await interaction.response.send_message(":x: Nenhum ticket encontrado para este canal.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(DeleteTicket(bot))
