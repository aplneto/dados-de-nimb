import os
import pages

import bot

token = os.getenv("TOKEN")

pages.go_online()
bot.bot.run(token)