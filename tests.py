# Max Markov 01.24.2023

import unittest
import shutil
import stat
import hashlib

from utility import *
from information_storage import Directory, File
from data_collector import handle_directory_file_system, collect_directory_data, collect_file_data
from input_validator import *
from database_manager import DatabaseManager


TEST_ROOT = 'test_data'
TEST_LOGGING = 'test_logging'

DEFAULT_STRUCTURE_ARGUMENT = os.path.join(TEST_ROOT, 'structure')
DEFAULT_DATABASE_ARGUMENT = os.path.join(TEST_ROOT, 'data.db')
DEFAULT_LOG_FILE_ARGUMENT = os.path.join(TEST_ROOT, 'log.txt')

DEFAULT_SCRIPT_ARGUMENTS = ['-d', DEFAULT_STRUCTURE_ARGUMENT, '-b', DEFAULT_DATABASE_ARGUMENT,
                            '-l', DEFAULT_LOG_FILE_ARGUMENT]
ARGUMENTS_DIRECTORY_POSITION = 1
ARGUMENTS_DATABASE_POSITION = 3
ARGUMENTS_LOG_POSITION = 5


class ArgumentValidationTestCase(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        """Remove all file structures generated while testing"""
        if os.path.isdir(TEST_ROOT):
            shutil.rmtree(TEST_ROOT, onerror=cls.on_deletion_error)

    def setUp(self):
        """Clears TEST_ROOT & resets script_arguments"""
        if os.path.isdir(TEST_ROOT):
            shutil.rmtree(TEST_ROOT, onerror=ArgumentValidationTestCase.on_deletion_error)
        os.makedirs(DEFAULT_STRUCTURE_ARGUMENT)
        self.script_arguments = DEFAULT_SCRIPT_ARGUMENTS.copy()

    @staticmethod
    def on_deletion_error(action, name, exception):
        os.chmod(name, stat.S_IRWXU)
        os.remove(name)

    def test_directory_missing(self):
        """Check if correct error is raised on directory missing"""
        self.script_arguments[ARGUMENTS_DIRECTORY_POSITION] = f'{DEFAULT_STRUCTURE_ARGUMENT}/missing_directory'
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


class DataCollectorTestCase(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        """Remove all file structures generated while testing"""
        if os.path.isdir(TEST_ROOT):
            shutil.rmtree(TEST_ROOT, onerror=cls.on_deletion_error)

    def setUp(self):
        """Clears TEST_ROOT & resets script_arguments"""
        if os.path.isdir(TEST_ROOT):
            shutil.rmtree(TEST_ROOT, onerror=DataCollectorTestCase.on_deletion_error)
        os.makedirs(DEFAULT_STRUCTURE_ARGUMENT)

    @staticmethod
    def on_deletion_error(action, name, exception):
        os.chmod(name, stat.S_IRWXU)
        os.remove(name)

    @staticmethod
    def create_missing_file(path):
        with open(path, 'x'):
            pass

    def test_handle_file_system_first(self):
        """Check if correct data collected form first directory configuration"""
        os.makedirs(f'{DEFAULT_STRUCTURE_ARGUMENT}/first/second')
        os.makedirs(f'{DEFAULT_STRUCTURE_ARGUMENT}/third')
        DataCollectorTestCase.create_missing_file(f'{DEFAULT_STRUCTURE_ARGUMENT}/first/file0.txt')
        DataCollectorTestCase.create_missing_file(f'{DEFAULT_STRUCTURE_ARGUMENT}/third/file1.txt')
        data = handle_directory_file_system(DEFAULT_STRUCTURE_ARGUMENT)
        self.assertEqual(len(data), 6)  # root, first, second, third, file0.txt, file1.txt
        self.assertIn('file0.txt', (element.name for element in data))
        self.assertIsInstance(data[0], Directory)  # root directory
        self.assertIsNone(data[0].parent)
        self.assertTrue(all(element.parent is not None for element in data[1:] if isinstance(element, Directory)))
        self.assertTrue(all(element.directory is not None for element in data if isinstance(element, File)))
        self.assertTrue(all(isinstance(element, Directory) or isinstance(element, File) for element in data))

    def test_handle_file_system_second(self):
        """Check if correct data collected form second directory configuration"""
        os.makedirs(f'{DEFAULT_STRUCTURE_ARGUMENT}/first/first/second/third')
        os.makedirs(f'{DEFAULT_STRUCTURE_ARGUMENT}/second')
        DataCollectorTestCase.create_missing_file(f'{DEFAULT_STRUCTURE_ARGUMENT}/first/file0.txt')
        DataCollectorTestCase.create_missing_file(f'{DEFAULT_STRUCTURE_ARGUMENT}/file1.txt')
        os.chmod(f'{DEFAULT_STRUCTURE_ARGUMENT}/file1.txt', stat.S_IREAD)
        DataCollectorTestCase.create_missing_file(f'{DEFAULT_STRUCTURE_ARGUMENT}/first/first/second/file2.txt')
        data = handle_directory_file_system(DEFAULT_STRUCTURE_ARGUMENT)
        self.assertEqual(len(data), 9)  # root, first, first, second, second, third, file0.txt, file1.txt, file2.txt
        self.assertNotIn('file3.txt', (element.name for element in data))
        self.assertIn('file2.txt', (element.name for element in data))
        self.assertIn('file1.txt', (element.name for element in data))
        self.assertIsInstance(data[0], Directory)  # root directory
        self.assertIsNone(data[0].parent)
        self.assertTrue(all(element.parent is not None for element in data[1:] if isinstance(element, Directory)))
        self.assertTrue(all(element.directory is not None for element in data if isinstance(element, File)))
        self.assertTrue(all(isinstance(element, Directory) or isinstance(element, File) for element in data))

    def test_handle_file_system_third(self):
        """Check if correct data collected form third directory configuration"""
        os.makedirs(f'{DEFAULT_STRUCTURE_ARGUMENT}/first')
        os.makedirs(f'{DEFAULT_STRUCTURE_ARGUMENT}/second/third/')
        os.makedirs(f'{DEFAULT_STRUCTURE_ARGUMENT}/fourth/fifth')
        DataCollectorTestCase.create_missing_file(f'{DEFAULT_STRUCTURE_ARGUMENT}/first/file0.txt')
        DataCollectorTestCase.create_missing_file(f'{DEFAULT_STRUCTURE_ARGUMENT}/second/file1.txt')
        DataCollectorTestCase.create_missing_file(f'{DEFAULT_STRUCTURE_ARGUMENT}/first/file2.txt')
        DataCollectorTestCase.create_missing_file(f'{DEFAULT_STRUCTURE_ARGUMENT}/fourth/fifth/file3.txt')
        os.chmod(f'{DEFAULT_STRUCTURE_ARGUMENT}/second/file1.txt', stat.S_IREAD)
        data = handle_directory_file_system(DEFAULT_STRUCTURE_ARGUMENT)
        root = collect_directory_data(f'{DEFAULT_STRUCTURE_ARGUMENT}', None)
        first = collect_directory_data(f'{DEFAULT_STRUCTURE_ARGUMENT}/first', root)
        second = collect_directory_data(f'{DEFAULT_STRUCTURE_ARGUMENT}/second', root)
        fourth = collect_directory_data(f'{DEFAULT_STRUCTURE_ARGUMENT}/fourth', root)
        third = collect_directory_data(f'{DEFAULT_STRUCTURE_ARGUMENT}/second/third', second)
        fifth = collect_directory_data(f'{DEFAULT_STRUCTURE_ARGUMENT}/fourth/fifth', fourth)
        file0 = collect_file_data(f'{DEFAULT_STRUCTURE_ARGUMENT}/first/file0.txt', first)
        file2 = collect_file_data(f'{DEFAULT_STRUCTURE_ARGUMENT}/first/file2.txt', first)
        file1 = collect_file_data(f'{DEFAULT_STRUCTURE_ARGUMENT}/second/file1.txt', second)
        file3 = collect_file_data(f'{DEFAULT_STRUCTURE_ARGUMENT}/fourth/fifth/file3.txt', fifth)
        manual_data = [root, first, second, fourth, third, fifth, file0, file2, file1, file3]
        self.assertTrue(all(any(manual_element == element for element in data) for manual_element in manual_data))


if __name__ == '__main__':
    unittest.main()
