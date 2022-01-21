import random
from Logical.Errors import InvalidArgumentsError

class MagischeMuschel():

    def __init__(self):
        pass

    def generateQuote(self, wann_frage):
        vielleicht_liste = [
            "morgen",
            "heute",
            "heute abend",
            "diese Woche",
            "diesen Monat",
            "dieses Jahr",
            "nach den Klausuren",
            "übermorgen"
        ]

        words_list = [
            f"Vielleicht {random.choice(vielleicht_liste)}",
            "Ja",
            "Nein",
            f"In {random.randint(1, 365)} Tage(n)",
            "Halt die Fresse",
            f"{random.randint(0, 10)} von 10 Ofenkäse",
            "Frag mich einfach nochmal",
            "Neeeeeeeeee",
            "EEEEEEEEEEEEEEEEEEEEEEEEH",
            "Gönn dir",
            "Heute nicht",
            "Frag Bunni",
            "Keine Ahnung aber wo ist eigentlich Truong?",
            "System.exit(1);",
            "Yallah",
            "Ja ehre",
            "Jetzt",
            "Wahrscheinlich",
            "Unwahrscheinlich",
            "Ja nech"
        ]
        if wann_frage:
            del words_list[0]
        return random.choice(words_list)

    def createRandom(self, lb, ub):
        if ub < lb:
            raise InvalidArgumentsError("[uB] < [lB] ist ungültig")
        return random.randint(lb, ub)
