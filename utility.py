# Max Markov 01.25.2023

import os
import hashlib


OCTAL_XYZ_RIGHTS_SLICE_START = -3
CHUNK_SIZE = 4096


class FileCanNotBeAccessedError(Exception):
    """Raised if database/log file can not be accessed"""
    MESSAGE = "File at {} cannot be accessed."

    def __init__(self, location: str):
        super().__init__(FileCanNotBeAccessedError.MESSAGE.format(location))


class FileCanNotBeCreatedError(Exception):
    """Raised if database/log file can not be created"""
    MESSAGE = "File at {} is missing and cannot be created."

    def __init__(self, location: str):
        super().__init__(FileCanNotBeCreatedError.MESSAGE.format(location))


def check_if_file_accessible(path: str):
    """Checks if information can be written inside the file
    :param path: Path to file check is being applied to
    :raise: FileCanNotBeAccessedError
    """
    if not os.access(path, os.W_OK):
        raise FileCanNotBeAccessedError(path)


def create_file_if_possible(path: str):
    """Creates file if there is a possibility of doing that
    NOTE: Assumes there is no such file in the first place
    :param path: Path to desired file
    :raise: FileCanNotBeCreatedError
    """
    try:
        open(path, 'x').close()
    except IOError:
        raise FileCanNotBeCreatedError(path)


def get_file_access_rights(file_mode: int) -> str:
    """Compiles list of available options for the file
    :param file_mode: st_mode of the file being processed
    :return: XYZ-format file access rights
    """
    return oct(file_mode)[OCTAL_XYZ_RIGHTS_SLICE_START:]


def calculate_file_sha256_hash(file_path: str) -> bytes:
    """Compute SHA256 hash of specified file content
    :param file_path: Path to file for hash calculation
    :return: SHA256 hash of file content as bytes
    """
    try:
        with open(file_path, 'rb') as file:
            file_hash = hashlib.sha256()
            while part := file.read(CHUNK_SIZE):
                file_hash.update(part)
            return file_hash.digest()
    except PermissionError:
        pass
