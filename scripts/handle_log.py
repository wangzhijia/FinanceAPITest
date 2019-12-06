import os
import time
import logging
from logging.handlers import RotatingFileHandler

from scripts.handle_config import do_config
from scripts.constants import LOGS_DIR

class HandleLog:
    """
    封装处理日志的类
    """
    def __init__(self):
        self.case_logger = logging.getLogger(do_config("log","logger_name"))

        self.case_logger.setLevel(do_config("log","logger_level"))

        console_handle = logging.StreamHandler()
        file_handle = RotatingFileHandler(filename=do_config("log","log_filename"),
                                          maxBytes=do_config("log","maxBytes"),
                                          backupCount=do_config("log","backupCount"),
                                          encoding="utf-8")

        console_handle.setLevel(do_config("log","console_level"))
        file_handle.setLevel(do_config("log","file_level"))

        simple_formatter = logging.Formatter(do_config("log","simple_formatter"))
        verbose_formatter = logging.Formatter(do_config("log","verbose_formatter"))

        console_handle.setFormatter(simple_formatter)
        file_handle.setFormatter(verbose_formatter)

        self.case_logger.addHandler(console_handle)
        self.case_logger.addHandler(file_handle)

    def get_logger(self):
        return self.case_logger


do_log = HandleLog().get_logger()

if __name__ == '__main__':
    pass



