import discord
from discord.ext import commands
from discord import app_commands

class UnbanSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unban", description="[⛔️] Desbane um membro do servidor.")
    @app_commands.describe(user_id="ID do usuário a ser desbanido", reason="Razão do desbanimento")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str, reason: str = None):
        try:
            # Converte o user_id de string para inteiro
            user_id_int = int(user_id)
            user = await self.bot.fetch_user(user_id_int)  # Obtem o usuário pelo ID
            await interaction.guild.unban(user, reason=reason)  # Tenta desbanir o usuário
            
            embed = discord.Embed(
                title=":white_check_mark: Membro desbanido!",
                description=f"{user.name} foi desbanido do servidor.",
                color=0x00ff00
            )
            if reason:
                embed.add_field(name="Razão", value=reason, inline=True)  # Adiciona razão se fornecida
            await interaction.response.send_message(embed=embed)
        except discord.NotFound:
            await interaction.response.send_message(":x: Usuário não encontrado. Verifique o ID e tente novamente.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message(":x: ID do usuário inválido. Verifique e tente novamente.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f":x: Ocorreu um erro ao tentar desbanir o membro: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(UnbanSlash(bot))
