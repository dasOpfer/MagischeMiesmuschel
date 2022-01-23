import muschel.logical.Commands as Commands
import muschel.logical.JSON_Reader as JSON_Reader
from discord.ext import commands

reader = JSON_Reader.Reader("../media/JSON/credentials.json")
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
