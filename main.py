import os
import pages

from discord.ext import commands

from db_bot import RPGDatabaseBot

token = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="!")
bot.add_cog(RPGDatabaseBot(bot, "rolagens.db"))

@bot.command(name="testar")
async def testando(ctx):
    await ctx.send(ctx.channel.id)
    await ctx.send(ctx.guild.id)

pages.go_online()

bot.run(token)