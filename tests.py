# Max Markov 01.24.2023

import unittest
import shutil
import stat

from utility import *
from messaging import *
from data_collector import handle_directory_file_system
from input_validator import *
from database_manager import DatabaseManager


TEST_ROOT = 'test_data'
TEST_LOGGING = 'test_logging'

DEFAULT_SCRIPT_ARGUMENTS = ['-d', TEST_ROOT, '-b', os.path.join(TEST_ROOT, 'data.db'),
                            '-l', os.path.join(TEST_ROOT, 'log.txt')]
ARGUMENTS_DIRECTORY_POSITION = 1
ARGUMENTS_DATABASE_POSITION = 3
ARGUMENTS_LOG_POSITION = 5


class NormalTestCase(unittest.TestCase):
    def setUp(self) -> None:
        """Clears TEST_ROOT & resets script_arguments"""
        if os.path.isdir(TEST_ROOT):
            shutil.rmtree(TEST_ROOT, onerror=NormalTestCase.on_deletion_error)
        os.makedirs(TEST_ROOT)
        self.script_arguments = DEFAULT_SCRIPT_ARGUMENTS

    @staticmethod
    def on_deletion_error(action, name, exception):
        os.chmod(name, stat.S_IRWXU)
        os.remove(name)

    def test_directory_missing(self):
        """Check if correct error is raised on directory missing"""
        self.script_arguments[ARGUMENTS_DIRECTORY_POSITION] = f'{TEST_ROOT}/missing_directory'
        arguments, not_parsed = ConsoleArgumentParser().parse_known_args(args=self.script_arguments)
        self.assertRaises(DirectoryMissingError, validate_input, arguments, not_parsed)

    def test_database_inaccessible(self):
        """Check if correct error is raised on read-only database"""
        test_db_path = f'{TEST_ROOT}/inaccessible.db'
        create_file_if_possible(test_db_path)
        os.chmod(test_db_path, stat.S_IREAD)
        self.script_arguments[ARGUMENTS_DATABASE_POSITION] = test_db_path
        arguments, not_parsed = ConsoleArgumentParser().parse_known_args(args=self.script_arguments)
        self.assertRaises(FileCanNotBeAccessedError, validate_input, arguments, not_parsed)

    def test_database_not_creatable(self):
        """Check if correct error is raised when trying to create database in missing directory"""
        self.script_arguments[ARGUMENTS_DATABASE_POSITION] = f'{TEST_ROOT}/missing_directory/inaccessible.db'
        arguments, not_parsed = ConsoleArgumentParser().parse_known_args(args=self.script_arguments)
        self.assertRaises(FileCanNotBeCreatedError, validate_input, arguments, not_parsed)


if __name__ == '__main__':
    unittest.main()
