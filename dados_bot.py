'''
Script que controla todas os comandos relacionados a rolagens do bot
Use o RPGDatabaseBot caso também queira usar o banco de dados pra salvar rolagens customizadas
'''
from discord.ext import commands
from rolagens import Dados

import discord

class DadosBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.remove_command("help")
    
    @commands.command(name='rolar', help='Simula rolagem de dados')
    async def roll(self, ctx, string_dados, efeitos=''):
        '''
        Recebe os inputs da chamada de rolagem padrão, delegando as tarefas para a classe de Dados resolver
        '''
        rolagem = Dados.rolar(string_dados, efeitos)
        msg = DadosBot.formatar_output(ctx.author.nick, rolagem)
        await ctx.send(embed = msg)

    @staticmethod
    def formatar_output(usr, rolagem: dict):
        '''
        Formata outputs de rolagens e testes para envio para o servidor
        '''
        em = discord.Embed(title=":game_die:")
        if (rolagem.get('rolagem')):
            total = rolagem.get('valor')
            rolagens = rolagem.get('rolagens')
            mods = rolagem.get('mods')
            die = '+'.join([str(x) for x in rolagens + mods]).replace("++", "+").replace("+-", "-")
            em.description = f"{usr} rolou: {die} = {total}"
            if (rolagem.get('crit') == 1):
                em.colour = discord.Colour.green()
            elif (rolagem.get('crit') == -1):
                em.colour = discord.Colour.red()
            else:
                em.colour = discord.Colour.blue()
        else:
            sucessos = rolagem.get('sucessos')
            rolagens = rolagem.get('rolagens')
            if (sucessos > 0):
                em.description = f"{usr} rolou: {'+'.join([str(x) for x in rolagens])} = {sucessos} sucessos"
                em.colour = discord.Colour.green()
            else:
                em.description = f"{usr} rolou: {'+'.join([str(x) for x in rolagens])} = Falhou"
                em.colour = discord.Colour.red()
        return em

    @commands.group(invoke_without_command=True)
    async def ajuda(self, ctx):
        em = discord.Embed(
            title="Ajuda",
            description = "Use o comando !ajuda <comando> para maiores detalhes",
            colour = discord.Colour.from_rgb(255, 255, 0)
        )

        em.add_field(name="Dados", value="rolar")
        await ctx.send(embed = em)
    
    @ajuda.command()
    async def rolar(self, ctx):
        em = discord.Embed(
            title="Rolar",
            description="Faz a rolagem descrita pela string, pode conter dados, modificadores e operações de soma e subtração entre números e dados, além de opções avançadas de rolagem (veja a tabela adiante), retornando a soma dos valores. \nPode também ser usada para testes, podendo conter comparações matemáticas como \"<\" e \">\" e opções avançadas de rolagem e retorna a quantidade de sucessos resultante do teste",
            colour = discord.Colour.from_rgb(255, 255, 0)
        )
        em.add_field(name="Uso", value="!rolar <string> [efeitos]")
        em.add_field(name="opções", value="k, t, kl, th, cs, cf")
        em.add_field(name="efeitos", value="c, f")
        em.add_field(name="Exemplo", value="!rolar 1d6c5+2+1 c+2")
        await ctx.send(embed = em)

    @commands.command(name="help")
    async def help(self, ctx):
        await self.ajuda(ctx)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logado como "{0.user}""'.format(self.bot))
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.errors.CommandNotFound,)
        if isinstance(error, ignored):
            return

        resp = ""
        if isinstance(error, commands.errors.MissingRequiredArgument):
            resp = "Seu comando precisa de um argumento!"
        
        em = discord.Embed(title=":x:", colour=discord.Colour.red(), description=resp)
        await ctx.send(embed=em)
