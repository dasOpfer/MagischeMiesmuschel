from muschel import cfgs, log, __bot_logger__
import muschel.logical.Commands as Commands
from muschel.logical.Media_Reader import JSONReader
from discord.ext import commands
import os

reader = JSONReader(os.path.join("..", "media", "json", "credentials.json"))
bot = commands.Bot(command_prefix=reader.getFileAttribute('prefix'))
bot.add_cog(Commands.Common())


@bot.event
async def on_ready():
    log.info("Bot ist online")


def run_bot():
    token = cfgs.getConfig("TOKEN")
    if not token:
        raise ValueError("Discord bot token empty")
    try:
        bot.loop.run_until_complete(bot.start(token))
    except KeyboardInterrupt:
        pass
    finally:
        bot.loop.run_until_complete(bot.close())
    return


def main():
    run_bot()
    log.info("Bot ist offline")
    return


if __name__ == '__main__':
    try:
        main()
    except (BaseException, Exception) as e:
        log.error(f"{type(e).__name__}: {e}", exc_info=True)
    __bot_logger__._stop_logging()
