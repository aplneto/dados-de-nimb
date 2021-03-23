import os
import pages

from discord.ext import commands

from db_bot import RPGDatabaseBot

token = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="!")
bot.add_cog(RPGDatabaseBot(bot, "rolagens.db"))

pages.go_online()

bot.run(token)