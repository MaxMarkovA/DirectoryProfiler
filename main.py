# Max Markov 01.24.2023

from argparse import ArgumentParser
import logging
from dataclasses import dataclass


PROGRAM_NAME = 'Directory Profiler'  # TODO here script name is required
PROGRAM_DESCRIPTION = ''  # TODO write appropriate program description


class ConsoleArgumentParser(ArgumentParser):
    """Console arguments handler based on argparse.ArgumentParser"""

    DIRECTORY_POSITIONAL = ('-d', '--directory')
    DIRECTORY_KEYWORD = {'required': True, 'help': 'path to the directory for inspection', 'metavar': 'DIRECTORY_PATH'}
    DATABASE_POSITIONAL = ('-b', '--database')
    DATABASE_KEYWORD = {'required': True, 'help': 'path to the database for gathered information',
                        'metavar': 'DATABASE_FILEPATH'}
    VERBOSE_POSITIONAL = ('-v', '--verbose')
    VERBOSE_KEYWORD = {'action': 'store_true', 'help': 'let process messages to appear in console'}
    LOGGING_POSITIONAL = ('-l', '--log')
    LOGGING_KEYWORD = {'required': True, 'help': 'path to the logging file for writing', 'metavar': 'LOGGING_FILEPATH'}

    def __init__(self):
        super().__init__(prog=PROGRAM_NAME, description=PROGRAM_DESCRIPTION)
        self.add_argument(*ConsoleArgumentParser.DIRECTORY_POSITIONAL, **ConsoleArgumentParser.DIRECTORY_KEYWORD)
        self.add_argument(*ConsoleArgumentParser.DATABASE_POSITIONAL, **ConsoleArgumentParser.DATABASE_KEYWORD)
        self.add_argument(*ConsoleArgumentParser.VERBOSE_POSITIONAL, **ConsoleArgumentParser.VERBOSE_KEYWORD)
        self.add_argument(*ConsoleArgumentParser.LOGGING_POSITIONAL, **ConsoleArgumentParser.LOGGING_KEYWORD)


class MessageWriter:
    """Logger with capability of console message display"""
    # TODO class should have special functions: 'write' & 'error' with message as a parameter

    FORMAT = "[%(asctime)s] %(levelname)s %(message)s"
    LEVEL = logging.INFO
    ENCODING = 'utf-8'

    def __init__(self, logging_file: str, verbose: bool):
        self.verbose = verbose
        logging.basicConfig(filename=logging_file, format=MessageWriter.FORMAT,
                            level=MessageWriter.LEVEL, encoding=MessageWriter.ENCODING)


@dataclass
class Directory:
    """Directory-related collected information"""


@dataclass
class File:
    """File-related collected information"""


def main():
    """Doin' Stuff..."""
    arguments, not_parsed = ConsoleArgumentParser().parse_known_args()


if __name__ == '__main__':
    main()
