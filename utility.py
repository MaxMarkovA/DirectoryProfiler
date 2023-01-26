# Max Markov 01.25.2023

import hashlib


OCTAL_XYZ_RIGHTS_SLICE_START = -3
CHUNK_SIZE = 4096


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
