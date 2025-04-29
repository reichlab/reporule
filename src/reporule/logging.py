"""reporule logging configuration."""

import logging
import os
import sys

import structlog


def setup_logging():
    shared_processors = [
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.processors.add_log_level,
    ]

    if sys.stderr.isatty():
        # If we're in a terminal, pretty print the logs.
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(),
        ]  # pragma: no cover
    else:
        # Otherwise, output logs in JSON format
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]

    # get log level from env variable or default to INFO
    level = os.environ.get("LOG_LEVEL", "INFO").upper()
    LOG_LEVEL = getattr(logging, level)

    structlog.configure(
        processors=processors,
        cache_logger_on_first_use=True,
        wrapper_class=structlog.make_filtering_bound_logger(LOG_LEVEL),
    )
