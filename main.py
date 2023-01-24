# Max Markov 01.24.2023

from argparse import ArgumentParser
import logging
from dataclasses import dataclass


PROGRAM_NAME = 'Directory Profiler'  # TODO here script name is required
PROGRAM_DESCRIPTION = ''  # TODO write appropriate program description


class ConsoleArgumentParser(ArgumentParser):
    """Console arguments handler based on argparse.ArgumentParser"""

    DIRECTORY_ARGUMENT = ('-d', '--directory')
    DATABASE_ARGUMENT = ('-b', '--database')
    VERBOSE_ARGUMENT = ('-v', '--verbose')
    LOGGING_ARGUMENT = ('-l', '--log')

    def __init__(self):
        super().__init__(prog=PROGRAM_NAME, description=PROGRAM_DESCRIPTION)
        self.add_argument(*ConsoleArgumentParser.DIRECTORY_ARGUMENT)
        self.add_argument(*ConsoleArgumentParser.DATABASE_ARGUMENT)
        self.add_argument(*ConsoleArgumentParser.VERBOSE_ARGUMENT, action='store_true')
        self.add_argument(*ConsoleArgumentParser.LOGGING_ARGUMENT)


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


if __name__ == '__main__':
    main()
