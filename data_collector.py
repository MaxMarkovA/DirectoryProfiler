# Max Markov 01.25.2023

from typing import Union
import os

import messaging
from utility import get_file_access_rights, calculate_file_sha256_hash
from information_storage import Directory, File


DIRECTORY_FOUND_MESSAGE_TEMPLATE = 'Found directory at: {}'
FILE_FOUND_MESSAGE_TEMPLATE = 'Found file at: {}'


def recursive_directory_walker(root_directory: str):
    """Performs bypass through directory content & generating file/directory locations
    NOTE: Based on 'Breadth first search' algorithm - see https://en.wikipedia.org/wiki/Breadth-first_search
    :param root_directory: Path to the starting directory for an algorithm
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
    :param path: Path to the processed file system element
    :return: Gathered information about directory elements
    """
    path = os.path.abspath(path)  # IMPORTANT: this also makes path windows-styled
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


def apply_data_collector(path: str, parent: Directory) -> Union[Directory, File]:
    """Based on element path decide which collector to call
    NOTE: This function also writes messages
    :param path: Path to current element
    :param parent: Parent directory for current element
    :return: Collected element data
    """
    if os.path.isdir(path):
        messaging.messanger.send_message(DIRECTORY_FOUND_MESSAGE_TEMPLATE.format(path))
        return collect_directory_data(path, parent)
    if os.path.isfile(path):
        messaging.messanger.send_message(FILE_FOUND_MESSAGE_TEMPLATE.format(path))
        return collect_file_data(path, parent)


def collect_directory_data(directory_path: str, parent: Directory) -> Directory:
    """Gathers data about specified directory & creates Directory from it
    :param directory_path: Path to the file system element proven to be a directory
    :param parent: Parent Directory
    :return: Directory object based on gathered data
    """
    return Directory(os.path.basename(directory_path), parent)


def collect_file_data(file_path: str, directory: Directory) -> File:
    """Gathers data about specified file & creates File from it
    :param file_path: Path to the file system element proven to be a file
    :param directory: Directory which this file is stored in
    :return: File object based on gathered data
    """
    file_statistics = os.stat(file_path)
    return File(os.path.basename(file_path), file_statistics.st_mtime, get_file_access_rights(file_statistics.st_mode),
                calculate_file_sha256_hash(file_path), directory)
