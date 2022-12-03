from muschel.utils.cfg_loader import _ConfigLoader
from muschel.utils.logger import _Logger
from discord import version_info as discord_ver
from sys import version_info as py_ver
from logging import getLogger

print("===================")
print(f"Python: v{py_ver.major}.{py_ver.minor}.{py_ver.micro}")
print(f"Discord: v{discord_ver.major}.{discord_ver.minor}.{discord_ver.micro}")
print("===================")

# Start terminal logging
log = getLogger(__name__)  # global usable logger
__bot_logger__ = _Logger()
__bot_logger__._setup_logger()

# Initialize configs
cfgs = _ConfigLoader()
cfgs._load_env_content()
