from datetime import datetime
from discord.ext import commands
from . import Muschel, Errors
from logging import getLogger

log = getLogger(__name__)


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
        try:
            await ctx.send(self.muschel.createRandom(int(lB), int(uB)))
        except ValueError:
            await ctx.send("Parameter müssen int sein")
        except Errors.InvalidArgumentsError:
            await ctx.send("uB muss größer gleich (>=) lB sein")
        except (Exception, BaseException) as e:
            await ctx.send(f"oopsie woopsie sowwy TwT\n{e}")

    @commands.command(name="decide", brief="Zufaellige Auswahl eines Parameters", description="Anwendungsbeispiel:\n!decide a b")
    async def decide(self, ctx, *args):
        try:
            await ctx.send(self.muschel.decideCell(args))
        except (Exception, BaseException) as e:
            await ctx.send(f"oopsie woopsie sowwy TwT\n{e}")

    @commands.command(name="uptime", brief="Gibt die Betriebszeit des Bots an")
    async def getUptime(self, ctx):
        try:
            await ctx.send(self.muschel.calcUptimeDelta(datetime.now()))
        except Errors.InvalidArgumentsError:
            await ctx.send("Mindestens Ein Parameter muss gegeben sein")
        except (Exception, BaseException) as e:
            await ctx.send(f"oopsie woopsie sowwy TwT\n{e}")

    @commands.command(name="exams", brief="Gibt die Zeit zwischen jetzt und der nachsten Prufungsphase an.")
    async def tellDeltaExams(self, ctx):
        try:
            d_hours = (int)(self.muschel.callExams() // 3600)
            d_days = (int)(self.muschel.callExams() // 86400)
            msg = f"Bis zur nächsten Klausurphase sind es noch {d_days} Tage | {d_hours} Stunden"
            await ctx.reply(msg)
        except (Exception, BaseException) as e:
            await ctx.send(f"oopsie woopsie sowwy TwT\n{e}")

    @commands.command()
    async def about(self, ctx):
        try:
            await ctx.send("help für mehr Informationen")
        except (Exception, BaseException) as e:
            await ctx.send(f"oopsie woopsie sowwy TwT\n{e}")

    @decide.error
    async def invalidArgs_decide_raise(self, ctx, error):
        if isinstance(error, commands.UnexpectedQuoteError):
            await ctx.send('https://media.discordapp.net/attachments/751138577567449220/936035020613763082/image0-1.gif')

    @getFrage.error
    async def invalidArgs_getFragen_raise(self, ctx, error):
        await ctx.send("https://img-9gag-fun.9cache.com/photo/aDDjdzd_460s.jpg")
        if isinstance(error, (commands.InvalidEndOfQuotedStringError, commands.MissingRequiredArgument)):
            await ctx.send("ich kann die Nachricht nicht lesen")
        elif isinstance(error, commands.UnexpectedQuoteError):
            await ctx.send('Sag das nochmal')

    @getRandom.error
    async def invalidArgs_getRandom_raise(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Ungültige/Fehlende Argumente. 2 sind gegeben.")


class ChatGPT(commands.Cog):

    def __init__(self, openai_api_key):
        self.muschel = Muschel.MagischeMuschel()
        self.gptSystem = ("Be yourself >:)")
        self.gptConversation = [{"role": "system", "content": self.gptSystem}]
        self.openAIKey = openai_api_key

    @commands.command(name="gpt", brief="Generiert Prompt von ChatGPT")
    async def callChatGPT(self, ctx):
        try:
            clean_msg = ctx.message.content.replace("!gpt", "")
            if clean_msg != "" and clean_msg is not None:
                self.gptConversation.append({"role": "user", "content": clean_msg})
                log.info(self.gptConversation)
                gptResponse = self.muschel.callGPTPrompt(self.gptConversation, self.openAIKey)
                self.gptConversation.append({"role": "assistant", "content": gptResponse})
                await ctx.reply(gptResponse)
            else:
                await ctx.reply("Bad Request")
        except (Exception, BaseException) as e:
            await ctx.send(f"oopsie woopsie sowwy TwT\n{e}")

    @commands.command(name="active_system", brief="Gibt die aktuellen Systemrestriktionen zurück.")
    async def getGPTSystem(self, ctx):
        try:
            await ctx.reply(f"currently active:\n\n{self.gptSystem}")
        except (Exception, BaseException) as e:
            await ctx.send(f"oopsie woopsie sowwy TwT\n{e}")

    @commands.command(name="gpt_system", brief="Erteilt dem ChatGPT-Bot Restriktionen, wie er sich verhalten soll")
    async def setGPTSystem(self, ctx):
        try:
            clean_msg = ctx.message.content.replace("!gpt_system", "")
            if (clean_msg != "" and clean_msg is not None):
                await ctx.reply(clean_msg)
            else:
                await ctx.reply("Bad Request")
        except (Exception, BaseException) as e:
            await ctx.send(f"oopsie woopsie sowwy TwT\n{e}")

    @commands.command(name="flush_gpt", brief="Loscht vorangegangene Konversationen und System-Restriktionen mit ChatGPT")
    async def flushChatGPT(self, ctx):
        try:
            self.gptSystem = ""
            self.gptConversation.clear()
            await ctx.reply("Flush erfolgreich")
        except (Exception, BaseException) as e:
            await ctx.send(f"oopsie woopsie sowwy TwT\n{e}")
