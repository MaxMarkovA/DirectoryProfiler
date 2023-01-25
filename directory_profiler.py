# Max Markov 01.24.2023


import logging

from input_validator import ConsoleArgumentParser
from data_collector import handle_directory_file_system


PROGRAM_NAME = 'Directory Profiler'
SCRIPT_START_MESSAGE = f'{PROGRAM_NAME} has started operating'
SCRIPT_FINAL_MESSAGE = f'{PROGRAM_NAME} has finished operating'

BASE_LOG = 'base_log.txt'


class MessageWriter:
    """Logger with capability of console message display"""
    # TODO combine two sending methods

    FORMAT = "[%(asctime)s] %(levelname)s %(message)s"
    LEVEL = logging.INFO
    ENCODING = 'utf-8'

    def __init__(self, logging_file: str, verbose: bool):
        self.verbose = verbose
        logging.basicConfig(filename=logging_file, format=MessageWriter.FORMAT,
                            level=MessageWriter.LEVEL, encoding=MessageWriter.ENCODING)

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


def main():
    """Doin' Stuff..."""
    arguments, not_parsed = ConsoleArgumentParser().parse_known_args()
    writer = MessageWriter(BASE_LOG, True)#arguments.log, arguments.verbose)
    writer.send_message(SCRIPT_START_MESSAGE)
    # TODO log arguments
    # TODO log mistakes with arguments
    # TODO check directory/file accessibility
    # TODO log paths to directories/files
    for element in handle_directory_file_system('test_data/00'):
        print(element)
    writer.send_message(SCRIPT_FINAL_MESSAGE)


if __name__ == '__main__':
    main()
