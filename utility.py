# Max Markov 01.25.2023

OCTAL_XYZ_RIGHTS_SLICE_START = -3


def get_file_access_rights(file_mode: int) -> str:
    """Compiles list of available options for the file
    :param file_mode: st_mode of the file being processed
    :return: XYZ-format file access rights
    """
    return oct(file_mode)[OCTAL_XYZ_RIGHTS_SLICE_START:]
