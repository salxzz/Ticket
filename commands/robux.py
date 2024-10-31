import discord
from discord.ext import commands

class Robux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # Definindo as embeds como atributos da classe
        self.embed1 = discord.Embed(
            title="💸 Robux 💸",
            description="Robux sem taxas",
            color=0xff0000  # Correção: Removidos os parênteses
        )
        self.embed1.add_field(name="**100:**", value="2.70 R$", inline=True)
        self.embed1.add_field(name="**200:**", value="5.40 R$", inline=True)
        self.embed1.add_field(name="**300:**", value="8.10 R$", inline=True)
        self.embed1.add_field(name="**400:**", value="10.80 R$", inline=True)
        self.embed1.add_field(name="**500:**", value="13.50 R$", inline=True)
        self.embed1.add_field(name="**1000:**", value="27 R$", inline=True)
        self.embed1.add_field(name="**2000:**", value="54 R$", inline=True)
        self.embed1.add_field(name="**3000:**", value="81 R$", inline=True)
        self.embed1.add_field(name="**4000:**", value="108 R$", inline=True)
        self.embed1.add_field(name="**5000:**", value="135 R$", inline=True)

        self.embed2 = discord.Embed(
            title="💸 Robux 💸",
            description="Robux com taxas",
            color=0xff0000  # Correção: Removidos os parênteses
        )
        self.embed2.add_field(name="**100:**", value="3.50 R$", inline=True)
        self.embed2.add_field(name="**200:**", value="7 R$", inline=True)
        self.embed2.add_field(name="**300:**", value="10.51 R$", inline=True)
        self.embed2.add_field(name="**400:**", value="14.01 R$", inline=True)
        self.embed2.add_field(name="**500:**", value="17.51 R$", inline=True)
        self.embed2.add_field(name="**1000:**", value="35 R$", inline=True)
        self.embed2.add_field(name="**2000:**", value="70 R$", inline=True)
        self.embed2.add_field(name="**3000:**", value="104 R$", inline=True)
        self.embed2.add_field(name="**4000:**", value="140 R$", inline=True)
        self.embed2.add_field(name="**5000:**", value="174 R$", inline=True)

    @commands.command()
    async def robuxs(self, ctx):
        await ctx.message.delete()
        await ctx.send(embed=self.embed1)
    
    @commands.command()
    async def robuxc(self, ctx):
        await ctx.message.delete()
        await ctx.send(embed=self.embed2)

# Função para adicionar o Cog ao bot
async def setup(bot):
    await bot.add_cog(Robux(bot))
