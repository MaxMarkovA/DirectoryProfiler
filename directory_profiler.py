# Max Markov 01.24.2023

from __future__ import annotations
from typing import Optional, Union
from dataclasses import dataclass

import os
from argparse import ArgumentParser
import logging
import hashlib


PROGRAM_NAME = 'Directory Profiler'
SCRIPT_NAME = 'directory_profiler.py'
PROGRAM_DESCRIPTION = 'Gather information about directory & write it into database'

SCRIPT_START_MESSAGE = f'{PROGRAM_NAME} has started operating'
SCRIPT_FINAL_MESSAGE = f'{PROGRAM_NAME} has finished operating'

BASE_LOG = 'base_log.txt'
CHUNK_SIZE = 4096


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


@dataclass
class Directory:
    """Directory-related collected information"""
    name: str
    parent: Optional[Directory]
    database_id: Optional[int] = None


@dataclass
class File:
    """File-related collected information"""
    name: str
    last_modified: float
    access_rules: str
    content_hash: hashlib.sha256
    directory: Directory


def recursive_directory_walker(root_directory: str):
    """Performs bypass through directory content & generating file/directory locations
    NOTE: Based on 'Breadth first search' algorithm - see https://en.wikipedia.org/wiki/Breadth-first_search
    :param root_directory: Absolute path to starting directory for an algorithm
    """
    recursion_stack = [(root_directory, None)]
    while recursion_stack:
        current_path, parent_directory = recursion_stack.pop(0)
        current_data = yield current_path, parent_directory
        if isinstance(current_data, Directory):
            for component in os.listdir(current_path):
                component = os.path.join(current_path, component)
                recursion_stack.append((component, current_data))


def handle_directory_file_system(path: str) -> list:
    """For each element in directory checks if it is a directory or a file & calls sufficient data collector
    :param path: Absolute path to processed file system element
    :return: Gathered information about directory elements
    """
    collected_elements = []
    data = None
    element_generator = recursive_directory_walker(path)
    while True:
        try:
            path, parent = element_generator.send(data)
        except StopIteration:
            break
        data = apply_data_collector(path, parent)
        collected_elements.append(data)
    return collected_elements


def apply_data_collector(path: str, parent: Directory) -> Union[File, Directory]:
    """Based on element path decide which collector to call
    :param path: Path to current element
    :param parent: Parent directory for current element
    :return: Collected element data
    """
    if os.path.isdir(path):
        return collect_directory_data(path, parent)
    if os.path.isfile(path):
        return collect_file_data(path, parent)


def collect_directory_data(directory_path: str, parent: Directory) -> Directory:
    """Gathers data about specified directory & creates Directory from it
    :param directory_path: Absolute path for file system element proven to be a directory
    :param parent: Parent Directory
    :return: Directory object based on gathered data
    """
    return Directory(os.path.basename(directory_path), parent)


def collect_file_data(file_path: str, directory: Directory) -> File:
    """Gathers data about specified file & creates File from it
    :param file_path: Absolute path for file system element proven to be a file
    :param directory: Directory which this file is stored in
    :return: File object based on gathered data
    """
    file_statistics = os.stat(file_path)
    return File(os.path.basename(file_path), file_statistics.st_mtime, oct(file_statistics.st_mode)[-3:],
                calculate_file_sha256_hash(file_path), directory)


def calculate_file_sha256_hash(file_path: str) -> hashlib.sha256:
    """Compute SHA256 hash of specified file content
    :param file_path: Path to file for hash calculation
    :return: SHA256 hash of file content
    """
    with open(file_path, 'rb') as file:
        file_hash = hashlib.sha256()
        while part := file.read(CHUNK_SIZE):
            file_hash.update(part)
        return file_hash


def main():
    """Doin' Stuff..."""
    arguments, not_parsed = ConsoleArgumentParser().parse_known_args()
    writer = MessageWriter(BASE_LOG, True)#arguments.log, arguments.verbose)
    writer.send_message(SCRIPT_START_MESSAGE)
    # TODO log arguments
    # TODO log mistakes with arguments
    # TODO check directory/file accessibility
    # TODO log paths to directories/files
    for element in handle_directory_file_system(os.path.abspath('test_data/00')):
        print(element)
    writer.send_message(SCRIPT_FINAL_MESSAGE)


if __name__ == '__main__':
    main()
