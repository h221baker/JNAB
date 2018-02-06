import logging


def get_logger(name):
    logger = logging.getLogger(name)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)
    return logger
