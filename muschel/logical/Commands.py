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
        self.openAIKey = openai_api_key
        self.rpEnabled = True

    @commands.command(name="gpt", brief="Generiert Prompt von ChatGPT")
    async def callChatGPT(self, ctx):
        try:
            clean_msg = ctx.message.content.replace("!gpt", "")
            if clean_msg != "" and clean_msg is not None:
                await ctx.reply(self.muschel.callGPTPrompt(clean_msg, ctx.message.author.name, self.openAIKey, rpEnabled=self.rpEnabled))
            else:
                await ctx.reply(self.muschel.callGPTPrompt("tell me how dumb i am", ctx.message.author.name, self.openAIKey, rpEnabled=self.rpEnabled))
        except (Exception, BaseException) as e:
            log.warning(e)

    @commands.command(name="toggle", brief="De/Aktiviert das Roleplay von ChatGPT und flusht Konversation")
    async def toggleRoleplay(self, ctx):
        try:
            self.rpEnabled = not self.rpEnabled
            self.muschel.flushGPTConversation()
            log.info("Roleplay: Enabled -> Disabled" if not self.rpEnabled else "Roleplay: Disabled -> Enabled")
            await ctx.reply("Roleplay: :clown: :point_right: :neutral_face:" if not self.rpEnabled else "Roleplay: :clown: :point_left: :neutral_face:")
        except (Exception, BaseException) as e:
            log.warning(e)


    @commands.command(name="flush", brief="Loscht vorangegangene Konversationen und System-Restriktionen mit ChatGPT")
    async def flushChatGPT(self, ctx):
        try:
            self.muschel.flushGPTConversation()
            await ctx.reply("Flush erfolgreich")
        except (Exception, BaseException) as e:
            log.warning(e)

    @commands.command(name="imagine", brief="Erstellt Bild mit DALL-E Mini")
    async def callGenerateImage(self, ctx):
        try:
            clean_msg = ctx.message.content.replace("!imagine", "")
            if clean_msg != "" and clean_msg is not None:
                gptAnswer = self.muschel.generateGPTImage(clean_msg, 2, self.openAIKey)
                for img_url in gptAnswer:
                    await ctx.send(img_url['url'])
            else:
                await ctx.reply(self.muschel.generateGPTImage('Clown Emoji pointing at Viewer', 1, self.openAIKey)[0]['url'])
        except (Exception, BaseException) as e:
            log.warning(e)
            await ctx.send(f"oopsie woopsie sowwy TwT\n{e}")
