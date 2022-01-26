import muschel.logical.Commands as Commands
from muschel.logical.Media_Reader import *
from discord.ext import commands

reader = JSONReader("../media/json/credentials.json")
bot = commands.Bot(command_prefix=reader.getFileAttribute('prefix'))
bot.add_cog(Commands.Common())


@bot.event
async def on_ready():
    print("bot ist bereit")


def run_bot():
    try:
        bot.loop.run_until_complete(bot.start(input("Token wo?: ")))
    except KeyboardInterrupt:
        pass
    finally:
        bot.loop.run_until_complete(bot.close())
    return


def main():
    run_bot()
    return


if __name__ == '__main__':
    try:
        main()
    except (BaseException, Exception) as e:
        print(f"{type(e).__name__}: {e}")
