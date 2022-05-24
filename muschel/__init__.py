from muschel.utils.cfg_loader import _ConfigLoader
from muschel.utils.logger import _Logger
from logging import getLogger

# Start terminal logging
log = getLogger(__name__)  # global usable logger
__bot_logger__ = _Logger()
__bot_logger__._setup_logger()

# Initialize configs
cfgs = _ConfigLoader()
cfgs._load_env_content()
