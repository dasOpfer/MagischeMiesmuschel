from logging import getLogger
import json
import os
from . import Errors

log = getLogger(__name__)


class MediaReader():

    def __init__(self, filepath):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, filepath)
        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename}: No such file or directory")
        if os.path.isdir(filename):
            raise IsADirectoryError("Target is a directory: " + filename)
        self.filepath = filename


class JSONReader(MediaReader):

    def __init__(self, filepath):
        super(JSONReader, self).__init__(filepath)
        self.__json_data = self.getJSONFromFile()

    def getJSONFromFile(self):
        if not self.filepath.lower().endswith("json"):
            raise Errors.InvalidFileEnding("Target is not a JSON file")
        json_file = {}
        try:
            with open(self.filepath, encoding="utf-8") as file:
                json_file = json.load(file)
            file.close()
        except Exception as e:
            log.error(f"Failed to read JSON file '{self.filepath}': {e}",
                      exc_info=True)
        return json_file

    def getFileAttribute(self, attr):
        try:
            if (self.__json_data[attr] == 0 or self.__json_data[attr]) == '':
                raise ValueError(f"{attr} besitzt den Wert 0 oder ''")
            return self.__json_data[attr]
        except KeyError:
            raise Exception(f"{attr} Attribut in Datei nicht gefunden")


#class IMGReader(MediaReader):
#   def __init__(self, filepath):
#        super(IMGReader, self).__init__(filepath)
#
#    def getIMGFromFile(self):
#        loweredFilepath = self.filepath.lower()
#        if not (loweredFilepath.endswith("jpg") or
#                 loweredFilepath.endswith("jpeg") or
#                 loweredFilepath.endswith("png")):
#            raise Errors.InvalidFileEnding("Datei endet nicht mit jp(e)g/png")
