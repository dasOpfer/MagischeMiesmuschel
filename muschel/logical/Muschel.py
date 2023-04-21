import random
import os
import openai
from datetime import datetime

from logging import getLogger
from .Media_Reader import JSONReader
from . import Errors

log = getLogger(__name__)


class MagischeMuschel():

    def __init__(self):
        self.initTime = datetime.now()
        self.reader = JSONReader(
            os.path.join("..", "media", "json", "credentials.json"))
        self.gptreader = JSONReader(
            os.path.join("..", "media", "json", "gptRoles.json"))
        self.gptMessages = [self.getGPTDefault()]
        self.latestMessage = self.initTime

    def generateQuote(self, wann_frage):
        vielleicht_liste = self.reader.getFileAttribute('vielleicht_list')
        words_liste = self.reader.getFileAttribute('words_list')
        res_word = random.choice(words_liste)
        if not wann_frage:
            if 'Vielleicht' in words_liste:
                words_liste.remove('Vielleicht')  # 'Vielleicht Ja Ehre' doesnt make sense...
        if res_word.lower() == ("vielleicht" or "vielleicht "):
            res_word += f" {random.choice(vielleicht_liste)}"
        elif res_word.lower() == "in":
            res_word += f" {random.randint(1, 365)} Tage(n)"
        # elif res_word.lower() == "von 10 ofenkäse":
        #     res_word = f"{random.randint(0, 10)} {res_word}"
        return res_word

    def createRandom(self, lb, ub):
        if ub < lb:
            raise Errors.InvalidArgumentsError("[uB] < [lB] ist ungültig")
        return random.randint(lb, ub)

    def calcTimeDelta(self, start_datetime, end_datetime):
        if start_datetime > end_datetime:
            start_datetime, end_datetime = end_datetime, start_datetime  # swap
        return end_datetime - start_datetime

    def calcUptimeDelta(self, o_datetime):
        return self.calcTimeDelta(self.initTime, o_datetime)

    def decideCell(self, args):
        if len(args) < 1:
            raise Errors.InvalidArgumentsError("Mindestens Ein Parameter muss gegeben sein")
        return random.choice(args)

    def callExams(self):
        now = datetime.now()
        year, month = now.year, 7
        if now.month >= 7:
            year, month = now.year + 1, 2
        then = datetime(year, month, 1, 0, 0, 0)
        return self.calcTimeDelta(now, then).total_seconds()

    def flushGPTConversation(self):
        self.gptMessages = [self.getGPTDefault()]

    def callGPTPrompt(self, msg: str, msg_author: str, apiKey: str, rpEnabled, timeout=600):
        """
        :param system: System Restriction Prompt. e.g ChatGPT DAN.
        :param msg: message (prompt) to chatGPT. will be added by self.gptConversation for context.
        :param apiKey: OpenAI-API Key.
        :param timeout: Timeout of latest Message from user. default 10 minutes
        :return: returns chatGPTs response to the ongoing Convo with the systemPrompt Restrictions.
        """
        try:
            openai.api_key = apiKey
            systemText = self.getGPTDefault()
            if (datetime.now() - self.latestMessage).total_seconds() >= timeout:
                self.flushGPTConversation()
            self.latestMessage = datetime.now()
            log.info(self.gptMessages)
            if not rpEnabled:
                systemText = "Be polite"
            else:
                msg = f"My name is {msg_author} - {msg}"
            self.gptMessages[0] = {"role": "system", "content": systemText}
            self.gptMessages.append({"role": "user", "content": msg})
            gptResponse = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.gptMessages
            )
            responseContent = gptResponse['choices'][0]['message']['content']
            self.gptMessages.append({"role": "assistant", "content": responseContent})  # adds answer from gpt for context
            return responseContent
        except (Exception, BaseException) as e:
            log.warning(e)

    def generateGPTImage(self, prmpt, amountImages, apiKey: str):
        try:
            if amountImages > 4:
                amountImages = 4
            elif amountImages < 1:
                amountImages = 1
            openai.api_key = apiKey
            gptResponse = openai.Image.create(
                prompt=f'"{prmpt}"',
                n=amountImages,
                size="1024x1024"
            )
            return gptResponse['data']
        except (Exception, BaseException) as e:
            log.warning(e)
            return e

    def getGPTDefault(self):
        try:
            return self.gptreader.getFileAttribute('gpt_system_default')
        except ValueError as e:
            log.warning(e)
