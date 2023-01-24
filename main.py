# Max Markov 01.24.2023

from argparse import ArgumentParser
import logging
from dataclasses import dataclass


PROGRAM_NAME = 'Directory Profiler'
PROGRAM_DESCRIPTION = ''  # TODO write appropriate program description


class ConsoleArgumentParser(ArgumentParser):
    """Console arguments handler based on argparse.ArgumentParser"""

    def __init__(self):
        super().__init__(prog=PROGRAM_NAME, description=PROGRAM_DESCRIPTION)
        # TODO here add_argument will be summoned multiple times for configuration purposes


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
