import random
from datetime import datetime

from .Media_Reader import JSONReader
from . import Errors


class MagischeMuschel():

    def __init__(self):
        self.initTime = datetime.now()

    def generateQuote(self, wann_frage):
        reader = JSONReader("../media/json/credentials.json")
        vielleicht_liste = reader.getFileAttribute('vielleicht_list')
        words_liste = reader.getFileAttribute('words_list')
        res_word = random.choice(words_liste)
        if (not wann_frage):
            words_liste.remove('Vielleicht')
        if res_word.lower() == ("vielleicht" or "vielleicht "):
            res_word += f" {random.choice(vielleicht_liste)}"
        elif res_word.lower() == "von 10 ofenkäse":
            res_word = {random.randint(0, 10)} + res_word
        elif res_word.lower() == "in":
            res_word += f" {random.randint(1, 365)} Tage(n)"
        return res_word

    # def generateQuote(self, wann_frage):
    #     vielleicht_liste = [
    #         "morgen",
    #         "heute",
    #         "heute abend",
    #         "diese Woche",
    #         "diesen Monat",
    #         "dieses Jahr",
    #         "nach den Klausuren",
    #         "übermorgen"
    #     ]
    #
    #     words_list = [
    #         f"Vielleicht {random.choice(vielleicht_liste)}",
    #         "Ja",
    #         "Nein",
    #         f"In {random.randint(1, 365)} Tage(n)",
    #         "Halt die Fresse",
    #         f"{random.randint(0, 10)} von 10 Ofenkäse",
    #         "Frag mich einfach nochmal",
    #         "Neeeeeeeeee",
    #         "EEEEEEEEEEEEEEEEEEEEEEEEH",
    #         "Gönn dir",
    #         "Heute nicht",
    #         "Frag Bunni",
    #         "Keine Ahnung aber wo ist eigentlich Truong?",
    #         "System.exit(1);",
    #         "Yallah",
    #         "Ja ehre",
    #         "Jetzt",
    #         "Wahrscheinlich",
    #         "Unwahrscheinlich",
    #         "Ja nech"
    #     ]
    #     if wann_frage:
    #         del words_list[0]
    #     return random.choice(words_list)

    def createRandom(self, lb, ub):
        if ub < lb:
            raise Errors.InvalidArgumentsError("[uB] < [lB] ist ungültig")
        return random.randint(lb, ub)

    def calcTimeDelta(self, o_datetime):
        return o_datetime - self.initTime

    def decideCell(self, args):
        if len(args) < 1:
            raise Errors.InvalidArgumentsError("Mindestens Ein Parameter muss gegeben sein")
        return random.choice(args)

    def callExams(self):
        now = datetime.now()
        year, month = now.year, 7
        if now.month > 7:
            year, month = now.year + 1, 2
        then = datetime(year, month, 1, 0, 0, 0)
        return (then - now).total_seconds()
        