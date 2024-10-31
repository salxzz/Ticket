import discord
from discord.ext import commands

class PingUserButton(discord.ui.Button):
    def __init__(self, user_id, label="PINGAR", emoji="📢", style=discord.ButtonStyle.primary, custom_id="ping_user_button"):
        super().__init__(label=label, emoji=emoji, style=style, custom_id=custom_id)
        self.user_id = user_id  # Armazenar o ID do usuário do ticket

    async def callback(self, interaction: discord.Interaction):
        # Menciona o usuário do ticket
        user = interaction.guild.get_member(self.user_id)
        if user:
            await interaction.response.send_message(f"{user.mention}, você foi mencionado!", ephemeral=False)
        else:
            await interaction.response.send_message(":x: Usuário não encontrado!", ephemeral=True)

