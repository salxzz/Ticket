import discord
from discord.ext import commands
from discord import app_commands

class ClearSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="[🪣] Remove um número de mensagens do canal.")
    @app_commands.describe(amount="Número de mensagens a serem removidas")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear_slash(self, interaction: discord.Interaction, amount: int):
        if amount < 2 or amount > 1000:
            await interaction.response.send_message("Por favor, insira um número entre 2 e 1000.", ephemeral=True)
            return

        # Indica que a resposta será enviada mais tarde
        await interaction.response.defer(ephemeral=True)

        # Purge messages, excluding pinned ones
        deleted = await interaction.channel.purge(limit=amount + 1, check=lambda m: not m.pinned)

        # Send response
        count_deleted = len(deleted) - 1  # Subtrair 1 para não contar a mensagem do comando
        if count_deleted > 0:
            await interaction.followup.send(f'{interaction.user.mention}, {count_deleted} mensagens foram deletadas.', ephemeral=True)
        else:
            await interaction.followup.send(f'{interaction.user.mention}, não havia mensagens para deletar.', ephemeral=True)

async def setup(bot):
    await bot.add_cog(ClearSlash(bot))
