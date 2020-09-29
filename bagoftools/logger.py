"""
Inspired from https://github.com/SebiSebi/friendlylog
"""

import logging
import sys
from copy import copy

from colored import attr, fg

DEBUG = "debug"
INFO = "info"
WARNING = "warning"
ERROR = "error"
CRITICAL = "critical"

LOG_LEVEL_LIST = [DEBUG, INFO, WARNING, ERROR, CRITICAL]


class _Formatter(logging.Formatter):

    def __init__(self, colorize=False, *args, **kwargs):
        super(_Formatter, self).__init__(*args, **kwargs)
        self.colorize = colorize

    @staticmethod
    def _process(msg, loglevel, colorize):
        loglevel = str(loglevel).lower()
        if loglevel not in LOG_LEVEL_LIST:
            raise RuntimeError(f"{loglevel} should be oneof {LOG_LEVEL_LIST}.")  # pragma: no cover

        msg = f"{str(loglevel).upper()}: {str(msg)}"

        if not colorize:
            return msg

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
        record.msg = _Formatter._process(record.msg, loglevel, self.colorize)
        return super(_Formatter, self).format(record)


class Logger:

    def __init__(self, name='default', colorize=False, stream=sys.stdout):
        self.name = name
        self.stream = stream

        # get the logger object; keep it hidden as there's no need to directly access it
        self.__logger = logging.getLogger(f"bagoftools.logger-{name}")
        self.__logger.setLevel(logging.DEBUG)
        self.__logger.propagate = False

        # use the custom formatter
        self.__formatter = _Formatter(
            colorize=colorize,
            fmt='[%(asctime)s.%(msecs)03d @ %(funcName)s] %(message)s',
            datefmt='%y-%m-%d %H:%M:%S'
        )

        self.__stream_handler = logging.StreamHandler(stream)
        self.__stream_handler.setFormatter(self.__formatter)

        self.__logger.handlers = []
        self.__logger.addHandler(self.__stream_handler)

        # install logging functions
        self.setLevel = self.__logger.setLevel
        self.debug = self.__logger.debug
        self.info = self.__logger.info
        self.warning = self.__logger.warning
        self.error = self.__logger.error
        self.critical = self.__logger.critical

    def log_function(self):
        def wrapper(func):
            def func_wrapper(*args, **kwargs):
                self.__logger.info(f'calling <{func.__name__}>\n\t  args: {args}\n\tkwargs: {kwargs}')
                out = func(*args, **kwargs)
                self.__logger.info(f'exiting <{func.__name__}>')

                return out

            return func_wrapper

        return wrapper

    # Don't use these unless you know what you are doing

    @property
    def inner_logger(self):
        return self.__logger

    @property
    def inner_stream_handler(self):
        return self.__stream_handler

    @property
    def inner_formatter(self):
        return self.__formatter
