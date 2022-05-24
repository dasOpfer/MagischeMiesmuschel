from dotenv import dotenv_values
from logging import getLogger
import os

log = getLogger(__name__)


class _ConfigLoader():
    def __init__(self):
        self.__env= os.path.join(".", "muschel", "config.env")
        self.__env_data = {}
        self.__config_loaded = False

    def _load_env_content(self):
        if self.__config_loaded:
            log.info("Configuration loaded already")
            return
        if not os.path.exists(self.__env) and not os.path.isfile(self.__env):
            log.warning("Configuration env not found!")
            return
        try:
            self.__env_data = dotenv_values(self.__env)
            self.__config_loaded = True
            log.info("Configurations loaded")
        except Exception as e:
            log.error(f"Failed to load env configurations: {e}", exc_info=True)
        return

    def getConfig(self, key: str, default = None):
        if not self.__config_loaded:
            return default
        return self.__env_data.get(key, default)
