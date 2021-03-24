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
        statement = 'INSERT OR REPLACE INTO rolagens (apelido, dados, g_id, c_id) VALUES (?, ?, ?, ?);'
        try:
            self.__cursor.execute(statement, (apelido, rolagem, ctx.author.guild.id, ctx.channel.id))
        except:
            resp = "Não foi possível salvar a sua rolagem"
        else:
            self.__db.commit()
            statement = 'SELECT rolagens.dados FROM rolagens WHERE rolagens.apelido = ? AND rolagens.g_id = ?;'
            self.__cursor.execute(statement, (apelido, ctx.author.guild.id))
            dado = self.__cursor.fetchone()
            resp = f'Rolagem "{apelido}" salva como "{dado[0]}"'
        em = discord.Embed(
            title=":game_die:",
            description = resp,
            colour=discord.Colour.from_rgb(255, 255, 0)
        )
        await ctx.send(embed=em)
            

    @commands.command(name='rolagem')
    async def executar_rolagem_salva(self, ctx, apelido: str):
        '''
        Tenta executar uma rolagem salva no banco de dados caso ela exista
        '''
        statement = 'SELECT rolagens.dados FROM rolagens WHERE rolagens.apelido = ? AND rolagens.g_id = ? AND rolagens.c_id = ?;'
        self.__cursor.execute(statement, (apelido, ctx.author.guild.id, ctx.channel.id))
        rolagem = self.__cursor.fetchone()
        if rolagem:
            await DadosBot.roll(self, ctx, *rolagem[0].split(' '))
        else:
            resp = f"Rolagem {apelido} não encontrada"
            await ctx.send(embed = discord.Embed(title=":game_die:", description=resp, colour=discord.Colour.from_rgb(255, 255, 0)))
    
    @commands.command(name='consultar')
    async def checar_rolagem_salva(self, ctx, apelido:str):
        '''
        Verifica se uma rola existe, enviando a formatação ao jogador caso exista
        '''
        statement = 'SELECT rolagens.dados FROM rolagens WHERE rolagens.apelido = ? AND rolagens.g_id = ? AND rolagens.c_id = ?;'
        self.__cursor.execute(statement, (apelido, ctx.author.guild.id, ctx.channel.id))
        rolagem = self.__cursor.fetchone()
        em = discord.Embed(title=":game_die:", colour=discord.Colour.from_rgb(255, 255, 0))
        if rolagem:
            em.add_field(name=f"{apelido}", value=f"\"{rolagem[0]}\"")
        else:
            em.description = f'Rolagem {apelido} não encontrada'
        await ctx.send(embed=em)

    @commands.command(name='rolagens')
    async def listar_rolagens_salvas(self, ctx):
        '''
        Lista todas as rolagens do canal salvas no banco de dados
        '''
        statement = 'SELECT rolagens.apelido, rolagens.dados FROM rolagens WHERE rolagens.g_id = ? AND rolagens.c_id = ?;'
        self.__cursor.execute(statement, (ctx.author.guild.id, ctx.channel.id))
        resultados = self.__cursor.fetchall()
        em = discord.Embed(title=":game_die:", description="Rolagens", colour=discord.Colour.from_rgb(255, 255, 0))
        for x in resultados:
            em.add_field(name=f"{x[0]}", value=f"\"{x[1]}\"")
        await ctx.send(embed=em)
        
    @commands.command(name='apagar')
    @commands.has_role("Mestre")
    async def apagar_rolagem_salva(self, ctx, apelido: str):
        '''
        Apaga uma rolagem salva do banco de dados
        '''
        statement = 'SELECT * FROM rolagens WHERE rolagens.apelido = apelido AND rolagens.g_id = ? AND rolagens.c_id = ?;'
        self.__cursor.execute(statement, (ctx.author.guild.id, ctx.channel.id))
        if len(self.__cursor.fetchall()) > 0:
            statement = 'DELETE FROM rolagens WHERE rolagens.apelido = ? AND rolagens.g_id = ? AND rolagens.c_id = ?;'
            self.__cursor.execute(statement, (apelido, ctx.author.guild.id, ctx.channel.id))
            resp = f'rolagem "{apelido}"" apagada com sucesso.'
            self.__db.commit()
        else:
            resp = f'rolagem "{apelido}" não encontrada.'
        await ctx.send(embed=discord.Embed(title=":game_die:", description=resp, colour=discord.Colour.from_rgb(255, 255, 0)))
    
    @commands.command(name="lembrar")
    @commands.has_role("Jogador")
    async def favoritar_rolagen(self, ctx, apelido, rolagem):
        '''
        Salva uma rolagem no banco de dados
        '''
        statement = 'INSERT OR REPLACE INTO favoritas (apelido, dados, u_id) VALUES (?, ?, ?);'
        try:
            self.__cursor.execute(statement, (apelido, rolagem, ctx.author.id))
        except:
            resp = "Não foi possível salvar a sua rolagem"
        else:
            self.__db.commit()
            statement = 'SELECT favoritas.dados FROM favoritas WHERE favoritas.apelido = ? AND favoritas.u_id = ?;'
            self.__cursor.execute(statement, (apelido, ctx.author.id))
            dado = self.__cursor.fetchone()
            resp = f'Rolagem "{apelido}" favoritada como "{dado[0]}"'
        em = discord.Embed(
            title=":star:",
            description = resp,
            colour=discord.Colour.from_rgb(255, 255, 0)
        )
        await ctx.send(embed=em)
    
    @commands.command(name="favoritas")
    @commands.has_role("Jogador")
    async def listar_favoritas(self, ctx):
        '''
        Lista todas as rolagens do canal salvas no banco de dados
        '''
        statement = 'SELECT favoritas.apelido, favoritas.dados FROM favoritas WHERE favoritas.u_id = ?;'
        self.__cursor.execute(statement, (ctx.author.id,))
        resultados = self.__cursor.fetchall()
        em = discord.Embed(title=":star:", description="Favoritas", colour=discord.Colour.from_rgb(255, 255, 0))
        for x in resultados:
            em.add_field(name=f"{x[0]}", value=f"\"{x[1]}\"")
        await ctx.send(embed=em)

    @commands.command(name='esquecer')
    @commands.has_role("Jogador")
    async def apagar_rolagem_favorita(self, ctx, apelido: str):
        '''
        Apaga uma rolagem salva do banco de dados
        '''
        statement = 'SELECT * FROM favoritas WHERE favoritas.apelido = ? AND favoritas.u_id = ?;'
        self.__cursor.execute(statement, (apelido, ctx.author.id))
        if len(self.__cursor.fetchall()) > 0:
            statement = 'DELETE FROM favoritas WHERE favoritas.apelido = ? AND favoritas.u_id = ?;'
            self.__cursor.execute(statement, (apelido, ctx.author.id,))
            resp = f'rolagem \"{apelido}\" esquecida.'
            self.__db.commit()
        else:
            resp = f"rolagem \"{apelido}\" não encontrada."
        await ctx.send(embed=discord.Embed(title=":star:", description=resp, colour=discord.Colour.from_rgb(255, 255, 0)))

    @commands.command(name='favorita')
    @commands.has_role("Jogador")
    async def executar_rolagem_favorita(self, ctx, apelido: str):
        '''
        Tenta executar uma rolagem salva no banco de dados caso ela exista
        '''
        statement = 'SELECT favoritas.dados FROM favoritas WHERE favoritas.apelido = ? AND favoritas.u_id = ?;'
        self.__cursor.execute(statement, (apelido, ctx.author.id))
        rolagem = self.__cursor.fetchone()
        if rolagem:
            await DadosBot.roll(self, ctx, *rolagem[0].split(' '))
        else:
            resp = f"Rolagem {apelido} não encontrada"
            await ctx.send(embed = discord.Embed(title=":star:", description=resp, colour=discord.Colour.from_rgb(255, 255, 0)))

    # Comandos de Ajuda
    
    @commands.group(invoke_without_command=True)
    async def ajuda(self, ctx):
        em = discord.Embed(
            title =":grey_question:",
            description = "Use o comando !ajuda <comando> para maiores detalhes",
            colour = discord.Colour.from_rgb(255, 255, 0)
        )

        em.add_field(name="Dados", value="rolar")
        em.add_field(
            name = "Rolagens da mesa",
            value = "rolagem, rolagens, consultar, salvar, apagar"
        )
        em.add_field(
            name = "Rolagens Individuais",
            value = " favorita, favoritas, lembrar, esquecer"
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
            description = "Salva uma rolagem específica com um apelido que pode ser usado por qualquer jogador naquele canal, mas apenas mestres podem usar esse comando. Caso uma rolagem já exista, seu valor é atualizado.",
            colour = discord.Colour.from_rgb(255, 255, 0)
        )
        em.add_field(name="Uso", value="!salvar \"<nome da rolagem>\" \"<rolagem>\"")
        em.add_field(name="Exemplo", value="!salvar \"Bola de fogo\" \"3d6cs4+4 c+3\"")

        await ctx.send(embed = em)

    @ajuda.command()
    async def apagar(self, ctx):
        em = discord.Embed(
            title = "Apagar",
            description = "Apaga uma rolagem salva no canal. Apenas mestres podem usar esse comando.",
            colour = discord.Colour.from_rgb(255, 255, 0)
        )
        em.add_field(name="Uso", value="!apagar \"<nome da rolagem>\"")
        em.add_field(name="Exemplo", value="!apagar \"Bola de fogo\"")

        await ctx.send(embed = em)
    
    @ajuda.command()
    async def favorita(self, ctx):
        em = discord.Embed(
            title = "Favorita",
            description = "Executa uma rolagem específica salva anteriormente por você.",
            colour = discord.Colour.from_rgb(255, 255, 0)
        )
        em.add_field(name="Uso", value="!favorita <nome da rolagem>\nVocê deve usar aspas se o nome da rolagem possuir espaços.")
        em.add_field(name="Exemplo", value="!favorita \"Ataque Especial\"")

        await ctx.send(embed = em)

    @ajuda.command()
    async def lembrar(self, ctx):
        em = discord.Embed(
            title = "Lembrar",
            description = "Salva uma rolagem específica com um apelido que pode ser usado por por você. Caso uma rolagem já exista, seu valor é atualizado.",
            colour = discord.Colour.from_rgb(255, 255, 0)
        )
        em.add_field(name="Uso", value="!lembrar \"<nome da rolagem>\" \"<rolagem>\"")
        em.add_field(name="Exemplo", value="!lembrar \"Ataque Especial\" \"2d20cs4+4 c+3\"")

        await ctx.send(embed = em)

    @ajuda.command()
    async def favoritas(self, ctx):
        em = discord.Embed(
            title = "Favoritas",
            description = "Lista todas as suas rolagens favoritas.",
            colour = discord.Colour.from_rgb(255, 255, 0)
        )
        em.add_field(name="Uso", value="!favoritas")

        await ctx.send(embed = em)

    @ajuda.command()
    async def esquecer(self, ctx):
        em = discord.Embed(
            title = "Esquecer",
            description = "Esquece uma rolagem salva por você.",
            colour = discord.Colour.from_rgb(255, 255, 0)
        )
        em.add_field(name="Uso", value="!esquecer \"<nome da rolagem>\"")
        em.add_field(name="Exemplo", value="!esquecer \"Ataque Especial\"")

        await ctx.send(embed = em)