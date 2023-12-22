import logging
import os

from rich.console import Console
from rich.logging import RichHandler

LOG_FORMAT_MSG = "%(message)s"
LOG_FORMAT_PID = "[PID %(process)d] - %(message)s"
LOG_FORMAT_FN  = "[%(funcName)s: %(lineno)d] - %(message)s"

CONSOLE = Console(color_system="256", width=150, style="blue")


class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # use my_context from kwargs or the default given on instantiation
        my_context = kwargs.pop('uuid', self.extra['uuid'])
        return '[%s] %s' % (my_context, msg), kwargs
    

def get_logger(module_name):
    logger = logging.getLogger(module_name)
    logger.propagate = False

    log_path = True
    log_format = LOG_FORMAT_FN

    handler = RichHandler(
        rich_tracebacks=False,
        console=CONSOLE,
        show_path=log_path
    )

    handler.setFormatter(logging.Formatter(log_format))
    
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger
