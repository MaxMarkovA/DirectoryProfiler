# Max Markov 01.24.2023

from argparse import ArgumentParser
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

    def __init__(self, verbose: bool):
        self.verbose = verbose
        # TODO here logger must be configured for writing messages which follow correct template


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
