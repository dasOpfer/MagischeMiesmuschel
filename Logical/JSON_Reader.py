import json
import os

class Reader():

    def __init__(self, filepath):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, filepath)
        if (os.path.isfile(filename) == False):
            raise FileNotFoundError("Datei Existiert nicht an: " + filename)
        else:
            self.filepath = filename

    def getJSON_from_File(self):
        with open(self.filepath) as f:
            return json.load(f)

    def getFileAttribute(self, attr):
        data = self.getJSON_from_File()
        try:
            if (data[attr] == 0 or data[attr]) == '':
                raise ValueError(f"{attr} besitzt den Wert 0 oder ''")
            return data[attr]
        except KeyError:
            raise Exception(f"{attr} Attribut in Datei nicht gefunden")