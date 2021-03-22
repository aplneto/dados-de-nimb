'''
Script que controla todas os comandos relacionados a rolagens do bot
'''
from discord.ext import commands

import dados

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print('Logado como "{0.user}""'.format(bot))

@bot.command(name='rolar', help='Simula rolagem de dados')
async def roll(ctx, string_dados):
    rolagem = dados.Dados.rolar(string_dados)
    msg = formatar_output(rolagem)
    await ctx.send(msg)

def formatar_output(rolagem: dict):
    if (rolagem.get('rolagem')):
        total = rolagem.get('valor')
        rolagens = rolagem.get('rolagens')
        mods = rolagem.get('mods')
        die = '+'.join([str(x) for x in rolagens+mods]).replace("++", "+").replace("+-", "-")
        return f":game_die:: {die} = {total}"
    else:
        sucessos = rolagem.get('sucessos')
        rolagens = rolagem.get('rolagens')
        return f":game_die:: {'+'.join([str(x) for x in rolagens])} = {sucessos} sucessos"