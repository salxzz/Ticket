import discord
from discord.ext import commands
import requests
import json

CANAL_ID = 1296639369150464061  # ID do canal onde o bot deve responder
API_KEY = "AIzaSyApMnpiMobydcC2zCabC9KiMZPA1v3SQHc"  # Sua chave da API da Gemini

class GeminiResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignora mensagens enviadas pelo próprio bot
        if message.author == self.bot.user:
            return

        # Ignora mensagens que começam com ','
        if message.content.startswith(','):
            return

        # Verifica se a mensagem foi enviada no canal especificado
        if message.channel.id == CANAL_ID:
            response = await self.get_gemini_response(message.content)
            if response:
                await self.send_response_in_parts(message.channel, response)

    async def get_gemini_response(self, prompt):
        # Adiciona uma instrução para responder apenas em português
        prompt_pt = f"Por favor, responda em português: {prompt}"
        
        api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt_pt
                        }
                    ]
                }
            ]
        }

        response = requests.post(api_url, headers=headers, json=data, params={'key': API_KEY})

        if response.status_code == 200:
            # Extrair a resposta do JSON
            data = response.json()
            # Removido o print da resposta da API
            
            # Corrigir o acesso à estrutura da resposta
            return data['candidates'][0]['content']['parts'][0]['text']  # Retorna a resposta
        else:
            print(f"Erro na requisição: {response.status_code} - {response.text}")
            await message.channel.send("Desculpe, ocorreu um erro ao processar sua solicitação.")
            return None

    async def send_response_in_parts(self, channel, response):
        max_length = 1500
        if len(response) > max_length:
            # Divide a resposta em partes de até 1500 caracteres
            parts = [response[i:i + max_length] for i in range(0, len(response), max_length)]
            for part in parts:
                await channel.send(part)
        else:
            await channel.send(response)

# Função para configurar o cog
async def setup(bot):
    await bot.add_cog(GeminiResponder(bot))
