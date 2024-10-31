import discord
import json
import config
import asyncio

class Excluir(discord.ui.Button):
    def __init__(self, label="EXCLUIR", emoji="🗑️", style=discord.ButtonStyle.red, custom_id="excluir_button"):
        super().__init__(label=label, emoji=emoji, style=style, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        # Carregar tickets existentes
        tickets = self.load_tickets()

        # Encontrar o ticket correspondente ao canal atual
        current_channel = interaction.channel
        ticket = next((ticket for ticket in tickets if ticket["channel_id"] == current_channel.id), None)

        if not ticket:
            await interaction.response.send_message("❌ Este canal não é um ticket ou já foi excluído.", ephemeral=True)
            return

        # Remover o ticket da lista e salvar as alterações
        tickets.remove(ticket)
        self.save_tickets(tickets)
        
        # Excluir o canal
        embed = discord.Embed(
            description="O ticket será deletado em alguns segundos...",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # Aguardar 3 segundos antes de enviar a mensagem de confirmação
        await asyncio.sleep(3)
        
        await interaction.followup.send("✔ Ticket está sendo excluído.", ephemeral=True)
        await asyncio.sleep(2)
        await current_channel.delete()

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

class ExcluirView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Excluir())
