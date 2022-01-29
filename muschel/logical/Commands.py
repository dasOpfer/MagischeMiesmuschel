import discord
from discord.ext import commands
from . import Muschel, Errors


class Common(commands.Cog):

    def __init__(self):
        self.muschel = Muschel.MagischeMuschel()

    @commands.command(name="ask", brief="Frage die Magische Miesmuschel Ja/Nein/wann Fragen")
    async def getFrage(self, ctx, *args):
        try:
            wann_frage = False
            searchQ = ""
            if True in ["wann" in x for x in args]:
                wann_frage = True
            for el in args:
                searchQ += (el + " ")
            await ctx.reply(self.muschel.generateQuote(wann_frage))
        except (Exception, BaseException) as e:
            await ctx.send(f"oopsie woopsie sowwy TwT\n{e}")

    @commands.command(name="random", brief="Zufallszahl zwischen [lB] und [uB] !random [lB] [uB]")
    async def getRandom(self, ctx, lB, uB):
        await ctx.send(self.muschel.createRandom(int(lB), int(uB)))

    @commands.command()
    async def about(self, ctx):
        try:
            await ctx.send("help für mehr Informationen")
        except ValueError:
            await ctx.send("Parameter müssen int sein")
        except (Exception, BaseException) as e:
            await ctx.send(f"oopsie woopsie sowwy TwT\n{e}")

    @getFrage.error
    async def invalidArgs_getFragen_raise(self, ctx, error):
        await ctx.send("https://img-9gag-fun.9cache.com/photo/aDDjdzd_460s.jpg")
        if isinstance(error, (commands.InvalidEndOfQuotedStringError or commands.MissingRequiredArgument)):
            await ctx.send("ich kann die Nachricht nicht lesen")

    @getRandom.error
    async def invalidArgs_getRandom_raise(self, ctx, error):
        print(type(error))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Ungültige/Fehlende Argumente. 2 sind gegeben.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("uB muss größer gleich (>=) lB sein")
