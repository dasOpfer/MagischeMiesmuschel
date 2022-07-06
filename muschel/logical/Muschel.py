import random
import os
from datetime import datetime

from .Media_Reader import JSONReader
from . import Errors


class MagischeMuschel():

    def __init__(self):
        self.initTime = datetime.now()
        self.reader = JSONReader(
            os.path.join("..", "media", "json", "credentials.json"))

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
