'''
Script que controla o Bot de rolagem com banco de dados
'''
import sqlite3
import discord

from discord.ext import commands
from dados_bot import DadosBot

class RPGDatabaseBot(DadosBot):
    def __init__(self, bot, db_name = "rolagens.db"):
        DadosBot.__init__(self, bot)
        self.__db = sqlite3.connect(db_name)
        self.__cursor = self.__db.cursor()
        self.__initialized = False
        self.__initializa_database()
    
    def __initializa_database(self, init_file = "db.sql"):
        with open("db.sql") as db_file:
            self.__cursor.executescript(db_file.read())
        self.__initialized = True

    @commands.command(name="salvar")
    @commands.has_role("Mestre")
    async def salvar_rolagem(self, ctx, apelido: str, rolagem: str):
        '''
        Salva uma rolagem no banco de dados
        '''
        statement = 'INSERT OR REPLACE INTO rolagens (apelido, dados, g_id) VALUES (?, ?, ?);'
        try:
            self.__cursor.execute(statement, (apelido, rolagem, ctx.author.guild.id))
        except:
            resp = "Não foi possível salvar a sua rolagem"
        else:
            self.__db.commit()
            statement = 'SELECT rolagens.dados FROM rolagens WHERE rolagens.apelido = ? AND rolagens.g_id = ?;'
            self.__cursor.execute(statement, (apelido, ctx.author.guild.id))
            dado = self.__cursor.fetchone()
            resp = f'Rolagem "{apelido}" salva como "{dado[0]}"'
        await ctx.send(resp)
            

    @commands.command(name='rolagem')
    async def executar_rolagem_salva(self, ctx, apelido: str):
        '''
        Tenta executar uma rolagem salva no banco de dados caso ela exista
        '''
        statement = 'SELECT rolagens.dados FROM rolagens WHERE rolagens.apelido = ? AND rolagens.g_id = ?;'
        self.__cursor.execute(statement, (apelido, ctx.author.guild.id))
        rolagem = self.__cursor.fetchone()
        if rolagem:
            await DadosBot.roll(self, ctx, *rolagem[0].split(' '))
        else:
            resp = f"Rolagem {apelido} não encontrada"
            await ctx.send(resp)
    
    @commands.command(name='consultar')
    async def checar_rolagem_salva(self, ctx, apelido:str):
        '''
        Verifica se uma rola existe, enviando a formatação ao jogador caso exista
        '''
        statement = 'SELECT rolagens.dados FROM rolagens WHERE rolagens.apelido = ? AND rolagens.g_id = ?;'
        self.__cursor.execute(statement, (apelido, ctx.author.guild.id))
        rolagem = self.__cursor.fetchone()
        if rolagem:
            resp = f':game_die: {apelido} -> {rolagem[0]}'
        else:
            resp = f'Rolagem {apelido} não encontrada'
        await ctx.send(resp)

    @commands.command(name='rolagens')
    async def listar_rolagens_salvas(self, ctx):
        '''
        Lista todas as rolagens do servidor salvas no banco de dados
        '''
        statement = 'SELECT rolagens.apelido, rolagens.dados FROM rolagens WHERE rolagens.g_id = ?;'
        self.__cursor.execute(statement, (ctx.author.guild.id,))
        resultados = self.__cursor.fetchall()
        resp = '\n'.join([f'"{x[0]}" -> "{x[1]}"' for x in resultados])
        await ctx.send(":game_die: Rolagens salvas :game_die:\n" + resp)
        
    @commands.command(name='apagar')
    @commands.has_role("Mestre")
    async def apagar_rolagem_salva(self, ctx, apelido: str):
        '''
        Apaga uma rolagem salva do banco de dados
        '''
        statement = 'DELETE FROM rolagens WHERE rolagens.apelido = apelido AND rolagens.g_id = ?'
        self.__cursor.execute(statement, (ctx.author.guild.id,))
        resp = f'rolagem {apelido} apagada com sucesso.'
        await ctx.send(resp)
        self.__db.commit()

    # Comandos de Ajuda
    
    @commands.group(invoke_without_command=True)
    async def ajuda(self, ctx):
        em = discord.Embed(
            title ="Ajuda",
            description = "Use o comando !ajuda <comando> para mais opções",
            url = 'https://dados-rpg-discord.paulinolimakl.repl.co?page=help',
            colour = discord.Colour.from_rgb(255, 255, 0)
        )

        em.add_field(name="Dados", value="rolar")
        em.add_field(
            name = "Salvos",
            value = "rolagem, rolagens, consultar, salvar, apagar"
        )
        await ctx.send(embed = em)
    
    @ajuda.command()
    async def rolagem(self, ctx):
        em = discord.Embed(
            title = "Rolagem",
            description = "Executa uma rolagem específica salva anteriormente pelo mestre.",
            colour = discord.Colour.from_rgb(255, 255, 0)
        )
        em.add_field(name="Uso", value="!rolagem <nome da rolagem>\nVocê deve usar aspas se o nome da rolagem possuir espaços.")
        em.add_field(name="Exemplo", value="!rolagem \"Bola de fogo\"")

        await ctx.send(embed = em)
    
    @ajuda.command()
    async def rolagens(self, ctx):
        em = discord.Embed(
            title = "Rolagens",
            description = "Lista todas as rolagens da mesa.",
            colour = discord.Colour.from_rgb(255, 255, 0)
        )
        em.add_field(name="Uso", value="!rolagens.")

        await ctx.send(embed = em)
    
    @ajuda.command()
    async def consultar(self, ctx):
        em = discord.Embed(
            title = "Consultar",
            description = "Procura pelo valor de uma rolagem específica, caso ela exista.",
            colour = discord.Colour.from_rgb(255, 255, 0)
        )
        em.add_field(name="Uso", value="!consultar <nome da rolagem>")
        em.add_field(name="Exemplo", value="!consultar \"Bola de fogo\"")

        await ctx.send(embed = em)
    
    @ajuda.command()
    async def salvar(self, ctx):
        em = discord.Embed(
            title = "Salvar",
            description = "Salva uma rolagem específica com um apelido que pode ser usado por qualquer jogador da mesa, mas apenas mestres podem usar esse comando. Caso uma rolagem já exista, seu valor é atualizado.",
            colour = discord.Colour.from_rgb(255, 255, 0)
        )
        em.add_field(name="Uso", value="!salvar \"<nome da rolagem>\" \"<rolagem>\"")
        em.add_field(name="Exemplo", value="!salvar \"Bola de fogo\" \"3d6cs4+4 c+3\"")

        await ctx.send(embed = em)

    @ajuda.command()
    async def apagar(self, ctx):
        em = discord.Embed(
            title = "Apagar",
            description = "Apaga uma rolagem salva na mesa. Apenas mestres podem usar esse comando.",
            colour = discord.Colour.from_rgb(255, 255, 0)
        )
        em.add_field(name="Uso", value="!apagar \"<nome da rolagem>\"")
        em.add_field(name="Exemplo", value="!apagar \"Bola de fogo\"")

        await ctx.send(embed = em)