'''
Script que controla todas os comandos relacionados a rolagens do bot
'''
from discord.ext import commands, tasks

import alpha.dados as dados

nimb = commands.Bot(command_prefix="!")

@nimb.event
async def on_ready():
    print('Logado como "{0.user}""'.format(nimb))

@nimb.command(name='rolar', help='Simula rolagem de dados')
async def roll(ctx, string_dados):
    rolagem = dados.Dados.rolar(string_dados)
    t = rolagem['valor']
    r = rolagem['rolagens']
    mods = rolagem['mods']
    die = '+'.join([str(x) for x in r+mods])
    die = die.replace("++", "+")
    die = die.replace("+-", "-")
    await ctx.send(f":game_die:: {die} = {t}")
    if rolagem['crit'] == 1:
      await ctx.send("Acerto crítico!")
    elif rolagem['crit'] == -1:
      await ctx.send("Falha crítica")

@nimb.command(name='testar', help='Simula um teste')
async def test(ctx, string_dados):
    sucessos, r, d = dados.Dados.testar(string_dados)
    await ctx.send(f":game_die:: {r} = {sucessos} sucessos")