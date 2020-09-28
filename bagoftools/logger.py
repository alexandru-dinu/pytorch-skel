"""
Borrowed from https://github.com/SebiSebi/friendlylog
"""

import logging
import sys

from colored import fg, attr
from copy import copy


DEBUG = "debug"
INFO = "info"
WARNING = "warning"
ERROR = "error"
CRITICAL = "critical"

LOG_LEVEL_LIST = [DEBUG, INFO, WARNING, ERROR, CRITICAL]

# Where the logs should be sent.
_STREAM = sys.stdout


class _Formatter(logging.Formatter):

    def __init__(self, *args, **kwargs):
        super(_Formatter, self).__init__(*args, **kwargs)

    @staticmethod
    def _colorize(msg, loglevel):
        loglevel = str(loglevel).lower()
        if loglevel not in LOG_LEVEL_LIST:
            raise RuntimeError(f"{loglevel} should be oneof {LOG_LEVEL_LIST}.") # pragma: no cover

        msg = f"{str(loglevel).upper()}: {str(msg)}"

        if loglevel == DEBUG:
            return "{}{}{}".format(fg(5), msg, attr(0))  # noqa: E501
        if loglevel == INFO:
            return "{}{}{}".format(fg(51), msg, attr(0))  # noqa: E501
        if loglevel == WARNING:
            return "{}{}{}{}{}".format(fg(214), attr(1), msg, attr(21), attr(0))  # noqa: E501
        if loglevel == ERROR:
            return "{}{}{}{}{}".format(fg(202), attr(1), msg, attr(21), attr(0))  # noqa: E501
        if loglevel == CRITICAL:
            return "{}{}{}{}{}".format(fg(196), attr(1), msg, attr(21), attr(0))  # noqa: E501

    def format(self, record):
        record = copy(record)
        loglevel = record.levelname
        record.msg = _Formatter._colorize(record.msg, loglevel)
        return super(_Formatter, self).format(record)


_logger = logging.getLogger("bagoftools.logger" + "-" + __name__)
_logger.propagate = False

_stream_handler = logging.StreamHandler(_STREAM)
_formatter = _Formatter(
        fmt='[%(asctime)s.%(msecs)03d @ %(funcName)s] %(message)s',
        datefmt='%y-%m-%d %H:%M:%S'
)
_stream_handler.setFormatter(_formatter)
_logger.addHandler(_stream_handler)
_logger.setLevel(logging.DEBUG)


# Export functions and objects.
inner_logger = _logger  # Don't use this except if you know what you are doing.
inner_stream_handler = _stream_handler  # Same thing for this object.
inner_formatter = _formatter  # Same thing for this object.


setLevel = _logger.setLevel
debug = _logger.debug
info = _logger.info
warning = _logger.warning
error = _logger.error
critical = _logger.critical


def log_function(logger):

    def wrapper(func):

        def func_wrapper(*args, **kwargs):
            logger.info(f'calling <{func.__name__}>\n\t  args: {args}\n\tkwargs: {kwargs}')
            out = func(*args, **kwargs)
            logger.info(f'exiting <{func.__name__}>')

            return out

        return func_wrapper

    return wrapper