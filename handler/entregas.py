# Arquivo: entregas.py

import discord
from discord.ui import View, Button
import json
import config
from handler.editproduto import EditProduto  # Importa a classe EditProduto
from handler.editimagem import AddImagem  # Importa a classe AddImagem
from handler.enviarentrega import EnviarEmbed

# Botão para postar entregas
class Entregas(discord.ui.Button):
    def __init__(self, allowed_role_id, label="POSTAR ENTREGA", emoji="📦", style=discord.ButtonStyle.green, custom_id="entrega_button"):
        super().__init__(label=label, emoji=emoji, style=style, custom_id=custom_id)
        self.allowed_role_id = allowed_role_id

    async def callback(self, interaction: discord.Interaction):
        # Verifica se o usuário tem permissão para usar o botão
        if self.allowed_role_id not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("❌ Você não tem permissão para usar este botão.", ephemeral=True)
            return

        # Busca as informações do ticket do usuário
        ticket_info = self.get_ticket_info(interaction.user.id)
        if not ticket_info:
            await interaction.response.send_message("❌ Não foi possível encontrar informações do ticket.", ephemeral=True)
            return

        cliente_nome = ticket_info["user_name"]
        produto_nome = ticket_info["product"]

        # Cria a embed com as informações do cliente e produto
        self.embed = discord.Embed(
            title="Shopbuxx Entregas",
            description=f"- 👤 Cliente: {cliente_nome}\n- 🛒 Produto: {produto_nome}",
            color=0xff0000,
        )

        # Envia a mensagem diretamente usando response e captura a mensagem enviada
        await interaction.response.send_message(embed=self.embed, ephemeral=True)
        msg = await interaction.original_response()  # Obtém a referência da mensagem enviada

        # Cria a view e adiciona os botões para editar o produto e adicionar a imagem
        view = EditProdutoView(self.embed, msg)

        # Edita a mensagem para adicionar a view com os botões Editar Produto e Adicionar Imagem
        await msg.edit(embed=self.embed, view=view)

    def get_ticket_info(self, user_id):
        """Busca as informações do ticket do usuário a partir do arquivo JSON."""
        try:
            # Abre o arquivo tickets.json para ler as informações
            with open("tickets.json", "r") as file:
                tickets = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

        # Procura por um ticket do usuário que esteja com status 'open'
        for ticket in tickets:
            if ticket["user_id"] == user_id and ticket["status"] == "open":
                return ticket
        return None


# View que contém os botões para editar o produto e adicionar a imagem
class EditProdutoView(discord.ui.View):
    def __init__(self, embed, message):
        super().__init__(timeout=None)
        self.add_item(EditProduto(embed, message))  # Adiciona o botão de edição de produto
        self.add_item(AddImagem(embed, message))
        self.add_item(EnviarEmbed())
        
        


# Cria a View principal com o botão de entrega
class EntregasView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Entregas(config.cargo_perm))  # Adiciona o botão de entrega principal
