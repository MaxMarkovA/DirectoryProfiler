# Max Markov 01.26.2023

import logging


BASE_LOG = 'base_log.txt'
DEFAULT_VERBOSE = False


class MessageWriter:
    """Logger with capability of console message display"""
    # TODO combine two sending methods

    FORMAT = "[%(asctime)s] %(levelname)s %(message)s"
    LEVEL = logging.INFO
    ENCODING = 'utf-8'

    def __init__(self, logging_file: str, verbose: bool):
        self.verbose = verbose
        logging.basicConfig(filename=logging_file, format=MessageWriter.FORMAT, level=MessageWriter.LEVEL,
                            force=True, encoding=MessageWriter.ENCODING)

    def send_message(self, message: str):
        """Log message & display it if verbose is enabled"""
        logging.info(message)
        if self.verbose:
            print(message)

    def send_error(self, message: str):
        """Log error message & display appropriate explanation"""
        logging.error(message)
        if self.verbose:
            print(message)


messanger = MessageWriter(BASE_LOG, DEFAULT_VERBOSE)
