import discord
from discord.ext import commands
import os
import json


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

with open('token.json', 'r') as arq:
    data = json.load(arq)
    token = data['token']
    
intents = discord.Intents.all()

class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", intents=intents)
    async def on_ready(self):
        clear_terminal()
        print(f'🔥 Logged in as {self.user}')
        print(f'ID: {self.user.id}')
        print('------------------------')

    async def setup_hook(self):
        for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'commands')):
            if filename.endswith('.py') and filename != '__init__.py':
                await self.load_extension(f'commands.{filename[:-3]}')
                    
        for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'commands/slashs')):
            if filename.endswith('.py') and filename != '__init__.py':
                await self.load_extension(f'commands.slashs.{filename[:-3]}')

client = MyClient()
client.run(token)
