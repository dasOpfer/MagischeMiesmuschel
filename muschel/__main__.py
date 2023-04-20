from muschel import cfgs, log, __bot_logger__
import muschel.logical.Commands as Commands
from muschel.logical.Media_Reader import JSONReader
from discord.ext import commands
import discord
import asyncio
import os

reader = JSONReader(os.path.join("..", "media", "json", "credentials.json"))
intents = discord.Intents.all()  # intent argument required for discord-py >2.0
bot = commands.Bot(command_prefix=reader.getFileAttribute('prefix'), intents=intents)


@bot.event
async def on_ready():
    log.info("Bot ist online")


async def run_bot():
    token = cfgs.getConfig("TOKEN")
    await bot.add_cog(Commands.Common())
    await bot.add_cog(Commands.ChatGPT(cfgs.getConfig("OPENAI_TOKEN")))
    if not token:
        raise ValueError("Discord bot token empty")
    await bot.start(token)
    return


async def main():
    await run_bot()
    if not bot.is_closed:
        await bot.close()
    log.info("Bot ist offline")
    return


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.warning(f"Caught KeyboardInterrupt. Bot forcefully stopped!")
    except (BaseException, Exception) as e:
        log.error(f"{type(e).__name__}: {e}", exc_info=True)
    __bot_logger__._stop_logging()
