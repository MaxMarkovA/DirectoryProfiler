# Max Markov 01.25.2023

import os
from argparse import Namespace, ArgumentParser
from typing import List

import messaging
from utility import check_if_file_accessible, create_file_if_possible


SCRIPT_NAME = 'directory_profiler.py'
PROGRAM_DESCRIPTION = 'Gather information about directory & write it into database'

ARGUMENTS_MESSAGE_TEMPLATE = 'Got arguments from console: {}'
LEFTOVER_ERROR_MESSAGE_TEMPLATE = 'Got some inputs which correspond to no actual arguments: {}'


class DirectoryMissingError(Exception):
    """Raised on missing directory for profiling"""
    MESSAGE = "Directory at {} is missing."

    def __init__(self, location: str):
        super().__init__(DirectoryMissingError.MESSAGE.format(location))


class NotAFileError(Exception):
    """Raised if database/log file is not a file"""
    MESSAGE = "Path {} does not lead to a file."

    def __init__(self, location: str):
        super().__init__(NotAFileError.MESSAGE.format(location))


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
        super().__init__(prog=SCRIPT_NAME, description=PROGRAM_DESCRIPTION)
        self.add_argument(*ConsoleArgumentParser.DIRECTORY_POSITIONAL, **ConsoleArgumentParser.DIRECTORY_KEYWORD)
        self.add_argument(*ConsoleArgumentParser.DATABASE_POSITIONAL, **ConsoleArgumentParser.DATABASE_KEYWORD)
        self.add_argument(*ConsoleArgumentParser.VERBOSE_POSITIONAL, **ConsoleArgumentParser.VERBOSE_KEYWORD)
        self.add_argument(*ConsoleArgumentParser.LOGGING_POSITIONAL, **ConsoleArgumentParser.LOGGING_KEYWORD)


def validate_input(arguments: Namespace, not_parsed: List[str]):
    """Check if input consists of valid arguments
    NOTE: This function writes messages
    :param arguments: Arguments parsed from console input
    :param not_parsed: Part which is missing correlation
    :raise: DirectoryMissingError
    """
    messaging.messanger.send_message(ARGUMENTS_MESSAGE_TEMPLATE.format(vars(arguments)))
    if not_parsed:
        messaging.messanger.send_error(LEFTOVER_ERROR_MESSAGE_TEMPLATE.format(not_parsed))
    if not os.path.exists(os.path.abspath(arguments.directory)):
        raise
    validate_file_for_writing(arguments.database)
    validate_file_for_writing(arguments.log)


def validate_file_for_writing(path: str):
    """Tries to create or access existing file
    :param path: Path to desired file
    :raise: NotAFileError
    """
    if os.path.exists(os.path.abspath(path)):
        if os.path.isfile(path):
            check_if_file_accessible(path)
    else:
        create_file_if_possible(path)
