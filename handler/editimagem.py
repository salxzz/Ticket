# Arquivo: editimagem.py

import discord
from discord.ui import Button, Modal, TextInput

# Botão para adicionar uma imagem à embed
class AddImagem(discord.ui.Button):
    def __init__(self, embed, message):
        super().__init__(label="ADICIONAR IMAGEM", emoji="🖼️", style=discord.ButtonStyle.secondary, custom_id="add_imagem_button")
        self.embed = embed
        self.message = message  # Armazena a referência da mensagem original

    async def callback(self, interaction: discord.Interaction):
        # Passa a embed e a mensagem para o modal
        modal = ImagemModal(self.embed, self.message)
        await interaction.response.send_modal(modal)


# Modal para adicionar a imagem na embed
class ImagemModal(Modal):
    def __init__(self, embed, message):
        super().__init__(title="Adicionar Imagem")
        self.embed = embed
        self.message = message  # Recebe a mensagem original para editar
        self.imagem_url = TextInput(
            label='URL da Imagem',
            placeholder='Cole a URL da imagem aqui...',
            required=True  # Torna obrigatório o preenchimento do campo
        )
        self.add_item(self.imagem_url)

    async def on_submit(self, interaction: discord.Interaction):
        url = self.imagem_url.value

        # Atualiza a embed com a URL da imagem fornecida
        self.embed.set_image(url=url)

        # Edita a mensagem original com a embed atualizada
        await self.message.edit(embed=self.embed)
        await interaction.response.send_message("✅ Imagem adicionada com sucesso!", ephemeral=True)
