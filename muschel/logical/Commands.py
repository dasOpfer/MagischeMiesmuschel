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
        except commands.InvalidEndOfQuotedStringError:
            # await ctx.send(file=discord.File())  # add File
            await ctx.send("Invalid End of Quotes")
        except (BaseException, Exception) as e:
            print(e)
            await ctx.send(f"oopsie woopsie sowwy TwT\n{e}")

    @commands.command(name="random", brief="Zufallszahl zwischen [lB] und [uB] !random [lB] [uB]")
    async def getRandom(self, ctx, lB, uB):
        try:
            await ctx.send(self.muschel.createRandom(int(lB), int(uB)))
        except discord.ext.commands.errors.MissingRequiredArgument:
            await ctx.send("Ungültige/Fehlende Argumente. 2 sind gegeben.")
        except Errors.InvalidArgumentsError:
            await ctx.send("uB muss größer gleich (>=) lB sein")
        except ValueError:
            await ctx.send("Parameter müssen int sein!")

    @commands.command()
    async def about(self, ctx):
        await ctx.send("help für mehr Informationen")
