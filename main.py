import os
from discord.ext import commands

import dados
from keep_alive import keep_alive

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print('Logado como "{0.user}""'.format(bot))

@bot.command(name='rolar', help='Simula rolagem de dados')
async def roll(ctx, string_dados):
    r, m, t = dados.decifrar_rolagem(string_dados)
    rolagem = '+'.join([str(x) for x in r+m])
    await ctx.send(f"{rolagem}={t}")

# keep_alive();
token = os.getenv("TOKEN")
bot.run(token)