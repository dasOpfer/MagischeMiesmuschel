import json
from Logical import Commands
from Logical import JSON_Reader
import discord
from discord.ext import commands, tasks

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def responding():
  return "i'm alive"

def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()


reader = JSON_Reader.Reader("../Media/JSON/credentials.json")
bot = commands.Bot(command_prefix=reader.getFileAttribute('prefix'))
bot.add_cog(Commands.Common(bot=bot))

@bot.event
async def on_ready():
    print("bot ist bereit")

@bot.command()
async def about(ctx):
    ctx.send("help für mehr Informationen")


if __name__ == '__main__':
    bot.run(input("Token eingeben: "))
    keep_alive()