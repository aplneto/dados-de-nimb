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
        em = DadosBot.formatar_output(ctx.author.nick, rolagem)
        await ctx.send(embed = em)

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
            r_final = []
            for i in range(len(rolagens)):
                dados = []
                for d in range(len(rolagens[i])):
                    if d < rolagem['validos'][i]:
                        dados.append(str(rolagens[i][d]))
                    else:
                        dados.append('~~'+str(rolagens[i][d])+'~~')
                r_final.append('['+', '.join(dados)+']')
            die = '+'.join([str(x) for x in r_final + mods]).replace("++", "+").replace("+-", "-")
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
            r_final = []
            for i in range(len(rolagens)):
                dados = []
                for d in range (len(rolagens[i])):
                    if d < rolagem['validos'][i]:
                        dados.append(str(rolagens[i][d]))
                    else:
                        dados.append('~~'+str(rolagens[i][d])+'~~')
                r_final.append('['+', '.join(dados)+']')
            if (sucessos > 0):
                s = 'sucessos' if sucessos > 1 else 'sucesso'
                em.description = f"{usr} rolou: {', '.join(r_final)} = {sucessos} {s}"
                em.colour = discord.Colour.green()
            else:
                em.description = f"{usr} rolou: {', '.join(r_final)} = Falhou"
                em.colour = discord.Colour.red()
        return em

    @commands.group(invoke_without_command=True)
    async def ajuda(self, ctx):
        msg, em = discord.Embed(
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
'''    
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
'''