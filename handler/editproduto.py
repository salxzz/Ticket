# Arquivo: editproduto.py

import discord
from discord.ui import Button, Modal, TextInput

# Botão para editar o nome do produto na embed
class EditProduto(discord.ui.Button):
    def __init__(self, embed, message):
        super().__init__(label="EDITAR PRODUTO", emoji="🛒", style=discord.ButtonStyle.primary, custom_id="editar_produto_button")
        self.embed = embed
        self.message = message  # Armazena a referência da mensagem original

    async def callback(self, interaction: discord.Interaction):
        # Passa a embed e a mensagem para o modal
        modal = ProdutoModal(self.embed, self.message)
        await interaction.response.send_modal(modal)


# Modal para editar o nome do produto
class ProdutoModal(Modal):
    def __init__(self, embed, message):
        super().__init__(title="Editar Produto")
        self.embed = embed
        self.message = message  # Recebe a mensagem original para editar
        self.produto_nome = TextInput(
            label='Nome do Produto',
            placeholder='Digite o nome do produto...',
            required=True
        )
        self.add_item(self.produto_nome)

    async def on_submit(self, interaction: discord.Interaction):
        produto = self.produto_nome.value

        # Atualiza a descrição da embed com o novo nome do produto
        self.embed.description = self.embed.description.split("\n")[0]  # Mantém apenas o cliente na descrição
        self.embed.description += f"\n- 🛒 Produto: {produto}"

        # Edita a mensagem original com a embed atualizada
        await self.message.edit(embed=self.embed)
        await interaction.response.send_message("✅ Produto atualizado com sucesso!", ephemeral=True)
