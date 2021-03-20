'''

'''

import os
from discord.ext import commands

import dados
from keep_alive import keep_alive

bot = commands.Bot(command_prefix="!")
d = dados.Dados()

@bot.event
async def on_ready():
    print('Logado como "{0.user}""'.format(bot))

@bot.command(name='rolar', help='Simula rolagem de dados')
async def roll(ctx, string_dados):
    t, r, mods = dados.Dados.rolar(string_dados)
    rolagem = '+'.join([str(x) for x in r+mods])
    rolagem = rolagem.replace("++", "+")
    rolagem = rolagem.replace("+-", "-")
    await ctx.send(f":game_die:: {rolagem} = {t}")

@bot.command(name='teste', help='Simula um teste')
async def test(ctx, string_dados):
  pass

# keep_alive();
token = os.getenv("TOKEN")
bot.run(token)