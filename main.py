# Max Markov 01.24.2023

from __future__ import annotations
from typing import Optional
from dataclasses import dataclass

from argparse import ArgumentParser
import logging
import hashlib


PROGRAM_NAME = 'Directory Profiler'  # TODO here script name is required
PROGRAM_DESCRIPTION = ''  # TODO write appropriate program description

SCRIPT_START_MESSAGE = f'{PROGRAM_NAME} has started operating'
SCRIPT_FINAL_MESSAGE = f'{PROGRAM_NAME} has finished operating'


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
    # TODO combine two sending methods

    FORMAT = "[%(asctime)s] %(levelname)s %(message)s"
    LEVEL = logging.INFO
    ENCODING = 'utf-8'

    def __init__(self, logging_file: str, verbose: bool):
        self.verbose = verbose
        logging.basicConfig(filename=logging_file, format=MessageWriter.FORMAT,
                            level=MessageWriter.LEVEL, encoding=MessageWriter.ENCODING)

    def send_message(self, message: str):
        """Log message & display it if verbose is enabled
        """
        logging.info(message)
        if self.verbose:
            print(message)

    def send_error(self, message: str):
        """Log error message & display appropriate explanation"""
        logging.error(message)
        if self.verbose:
            print(message)


@dataclass
class Directory:
    """Directory-related collected information"""
    name: str
    parent: Optional[Directory]


@dataclass
class File:
    """File-related collected information"""
    name: str
    last_modified: float
    access_rules: int
    content_hash: hashlib.sha256
    directory: Directory


def recursive_directory_walker(root_directory: str, max_depth: int):
    """Performs bypass through directory content & generating file/directory locations
    NOTE: Based on 'Breadth first search' algorithm - see https://en.wikipedia.org/wiki/Breadth-first_search
    :param root_directory: Absolute path to starting directory for an algorithm
    :param max_depth: Recursion limit representing maximum directory stacking
    """


def directory_file_system_handler(path: str):
    """For each element in directory checks if it is a directory or a file & calls sufficient data collector
    :param path: Absolute path to processed file system element
    :return: Gathered information about directory elements
    """


def file_data_collector(file_path: str, directory: Directory) -> File:
    """Gathers data about specified file & creates File from it
    :param file_path: Absolute path for file system element proven to be a file
    :param directory: Directory which this file is stored in
    :return: File object based on gathered data
    """


def directory_data_collector(directory_path: str, parent: Directory = None) -> File:
    """Gathers data about specified directory & creates Directory from it
    :param directory_path: Absolute path for file system element proven to be a directory
    :param parent: Parent Directory
    :return: File object based on gathered data
    """


def main():
    """Doin' Stuff..."""
    arguments, not_parsed = ConsoleArgumentParser().parse_known_args()
    writer = MessageWriter(arguments.log, arguments.verbose)
    writer.send_message(SCRIPT_START_MESSAGE)
    writer.send_message(SCRIPT_FINAL_MESSAGE)


if __name__ == '__main__':
    main()
