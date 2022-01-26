import json
import os
from .Errors import *

class MediaReader():

    def __init__(self, filepath):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, filepath)
        if (not os.path.isfile(filename)):
            raise FileNotFoundError("Datei Existiert nicht an: " + filename)
        else:
            self.filepath = filename

    def __repr__(self):
        print(f"My filepath: {self.filepath}")

class JSONReader(MediaReader):

    def __init__(self, filepath):
        super(JSONReader, self).__init__(filepath)

    def getJSONFromFile(self):
        if (not self.filepath.lower().endswith("json")):
            Errors.InvalidFileEnding("Datei endet nicht mit json")
        with open(self.filepath, encoding='utf-8') as f:
            return json.load(f)

    def getFileAttribute(self, attr):
        data = self.getJSONFromFile()
        try:
            if (data[attr] == 0 or data[attr]) == '':
                raise ValueError(f"{attr} besitzt den Wert 0 oder ''")
            return data[attr]
        except KeyError:
            raise Exception(f"{attr} Attribut in Datei nicht gefunden")


class IMGReader(MediaReader):
    
    def __init__(self, filepath):
        super(IMGReader, self).__init__(filepath)

    def getIMGFromFile(self):
        loweredFilepath = self.filepath.lower()
        if (not (loweredFilepath.endswith("jpg") or
                 loweredFilepath.endswith("jpeg") or
                 loweredFilepath.endswith("png"))):
            raise Errors.InvalidFileEnding("Datei endet nicht mit jp(e)g/png")
