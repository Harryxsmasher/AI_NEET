"""
=========================================
AI_NEET Logger

Author : Praveen Mark
=========================================
"""

import logging
import sys
from pathlib import Path

import colorlog

from core.constants import LOG_DIR


class Logger:

    _logger = None

    @classmethod
    def get_logger(cls):

        if cls._logger is not None:
            return cls._logger

        LOG_DIR.mkdir(exist_ok=True)

        logger = logging.getLogger("AI_NEET")

        logger.setLevel(logging.INFO)

        logger.handlers.clear()

        file_handler = logging.FileHandler(
            LOG_DIR / "ai_neet.log",
            encoding="utf-8"
        )

        file_handler.setLevel(logging.INFO)

        file_formatter = logging.Formatter(

            "%(asctime)s | %(levelname)s | %(message)s"

        )

        file_handler.setFormatter(file_formatter)

        console_handler = colorlog.StreamHandler(sys.stdout)

        console_handler.setLevel(logging.INFO)

        console_formatter = colorlog.ColoredFormatter(

            "%(log_color)s%(levelname)-8s%(reset)s %(message)s",

            log_colors={

                "DEBUG": "cyan",

                "INFO": "green",

                "WARNING": "yellow",

                "ERROR": "red",

                "CRITICAL": "bold_red"

            }

        )

        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)

        logger.addHandler(console_handler)

        cls._logger = logger

        return logger