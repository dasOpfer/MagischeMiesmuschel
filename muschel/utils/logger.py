import logging
import platform

_USE_ASNI_COLOR = True

if platform.system().lower() == "windows":
    try:
        import colorama
        colorama.init()
    except Exception:
        _USE_ASNI_COLOR = False


class Colors:
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RED_BG = "\033[101m"
    END = "\033[0m"


def setColor(text: str, color: Colors) -> str:
    if not _USE_ASNI_COLOR:
        return text  # do not set ASNI (on Windows)
    return f"{color}{text}{Colors.END}"


class LogColorFormatter(logging.Formatter):
    def format(self, logtype):
        LOG_FORMAT = "%(asctime)s - %(levelname)-8s - %(name)s: %(message)s"
        LOG_COLORS = {#"DEBUG": LOG_FORMAT,
                      "INFO": LOG_FORMAT,
                      "WARNING": setColor(LOG_FORMAT, Colors.YELLOW),
                      "ERROR": setColor(LOG_FORMAT, Colors.RED),
                      "CRITICAL": setColor(LOG_FORMAT, Colors.RED_BG)}
        get_type = LOG_COLORS.get(logtype.levelname)
        formatter = logging.Formatter(get_type,
                                      "%Y-%m-%d %H:%M:%S").format(logtype)
        return formatter


class _Logger:
    def __init__(self):
        self.__shandler = None

    def _setup_logger(self):
        self.__shandler = logging.StreamHandler()
        self.__shandler.setFormatter(LogColorFormatter())
        logging.basicConfig(handlers=[self.__shandler], level=logging.INFO)
        return

    def _stop_logging(self):
        if self.__shandler:
            self.__shandler.close()
        return
