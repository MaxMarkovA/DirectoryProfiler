# Max Markov 01.24.2023

import os.path
import unittest
import shutil
import stat
import sqlite3
from random import choices
from string import ascii_lowercase

from utility import *
from information_storage import Directory, File
from data_collector import handle_directory_file_system, collect_directory_data, collect_file_data
from input_validator import *
from database_manager import DatabaseManager


TEST_ROOT = 'test_data'
TEST_LOGGING = 'test_logging'

DEFAULT_STRUCTURE_ARGUMENT = os.path.join(TEST_ROOT, 'structure')  # subdirectory for profiling
DEFAULT_DATABASE_ARGUMENT = os.path.join(TEST_ROOT, 'data.db')  # database for storing results
DEFAULT_LOG_FILE_ARGUMENT = os.path.join(TEST_ROOT, 'log.txt')  # test-log which is not tested

DEFAULT_SCRIPT_ARGUMENTS = ['-d', DEFAULT_STRUCTURE_ARGUMENT, '-b', DEFAULT_DATABASE_ARGUMENT,
                            '-l', DEFAULT_LOG_FILE_ARGUMENT]
ARGUMENTS_DIRECTORY_POSITION = 1
ARGUMENTS_DATABASE_POSITION = 3
ARGUMENTS_LOG_POSITION = 5

DATABASE_READ_DIRECTORIES = 'SELECT * FROM directories'
DATABASE_READ_FILES = 'SELECT * FROM files'
DIRECTORY_RECORD_ID_INDEX = 0
DIRECTORY_RECORD_PARENT_INDEX = 1
DIRECTORY_RECORD_NAME_INDEX = 2
FILE_RECORD_DIRECTORY_INDEX = 1
FILE_RECORD_NAME_INDEX = 2


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
        """Perform access rights change for a read-only file & delete it"""
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

    def test_normal_arguments(self):
        """Check if arguments are parsed correctly in some average scenario"""
        arguments, not_parsed = ConsoleArgumentParser().parse_known_args(args=self.script_arguments)
        manual_arguments = {'directory': DEFAULT_STRUCTURE_ARGUMENT, 'database': DEFAULT_DATABASE_ARGUMENT,
                            'verbose': False, 'log': DEFAULT_LOG_FILE_ARGUMENT}
        self.assertEqual(vars(arguments), manual_arguments)
        self.assertFalse(not_parsed)


class DataCollectorTestCase(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        """Remove all file structures generated while testing"""
        if os.path.isdir(TEST_ROOT):
            shutil.rmtree(TEST_ROOT, onerror=cls.on_deletion_error)

    def setUp(self):
        """Clears TEST_ROOT"""
        if os.path.isdir(TEST_ROOT):
            shutil.rmtree(TEST_ROOT, onerror=DataCollectorTestCase.on_deletion_error)
        os.makedirs(DEFAULT_STRUCTURE_ARGUMENT)

    @staticmethod
    def on_deletion_error(action, name, exception):
        """Perform access rights change for a read-only file & delete it"""
        os.chmod(name, stat.S_IRWXU)
        os.remove(name)

    @staticmethod
    def create_missing_file(path):
        """Create file which location is not occupied & specified by path"""
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
        file1 = collect_file_data(f'{DEFAULT_STRUCTURE_ARGUMENT}/second/file1.txt', second)
        file2 = collect_file_data(f'{DEFAULT_STRUCTURE_ARGUMENT}/first/file2.txt', first)
        file3 = collect_file_data(f'{DEFAULT_STRUCTURE_ARGUMENT}/fourth/fifth/file3.txt', fifth)
        manual_data = [root, first, second, fourth, third, fifth, file0, file2, file1, file3]
        self.assertTrue(all(any(manual_element == element for element in data) for manual_element in manual_data))


class UtilityTestCase(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        """Remove all file structures generated while testing"""
        if os.path.isdir(TEST_ROOT):
            shutil.rmtree(TEST_ROOT, onerror=cls.on_deletion_error)

    def setUp(self):
        """Clears TEST_ROOT"""
        if os.path.isdir(TEST_ROOT):
            shutil.rmtree(TEST_ROOT, onerror=UtilityTestCase.on_deletion_error)
        os.makedirs(TEST_ROOT)

    @staticmethod
    def on_deletion_error(action, name, exception):
        """Perform access rights change for a read-only file & delete it"""
        os.chmod(name, stat.S_IRWXU)
        os.remove(name)

    @staticmethod
    def create_and_fill_file(path, content):
        """Create file at specified location & fill it with text content"""
        with open(path, 'wb') as file:
            file.write(content)

    @staticmethod
    def generate_random_string(length):
        """Creates randomly composed string from ASCII lowercase characters"""
        return ''.join(choices(ascii_lowercase, k=length))

    def test_normal_file_hash_calculation(self):
        """Calculate hash for a file with read permission"""
        test_file = f'{TEST_ROOT}/test_file.txt'
        file_content = 'test file content repeat: test file content'.encode('utf-8')
        UtilityTestCase.create_and_fill_file(test_file, file_content)
        self.assertEqual(calculate_file_sha256_hash(test_file), hashlib.sha256(file_content).digest())

    def test_huge_file_hash_calculation(self):
        """Calculate hash for a file with not-single-chunked content"""
        test_file = f'{TEST_ROOT}/test_file.txt'
        file_content = UtilityTestCase.generate_random_string(10000).encode('utf-8')
        UtilityTestCase.create_and_fill_file(test_file, file_content)
        self.assertEqual(calculate_file_sha256_hash(test_file), hashlib.sha256(file_content).digest())


class DatabaseManagerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Clears TEST_ROOT & sets up directory file system"""
        if os.path.isdir(TEST_ROOT):
            shutil.rmtree(TEST_ROOT, onerror=DatabaseManagerTestCase.on_deletion_error)
        os.makedirs(DEFAULT_STRUCTURE_ARGUMENT)
        os.makedirs(f'{DEFAULT_STRUCTURE_ARGUMENT}/first')
        os.makedirs(f'{DEFAULT_STRUCTURE_ARGUMENT}/second/third')
        os.makedirs(f'{DEFAULT_STRUCTURE_ARGUMENT}/fourth/fifth')
        DatabaseManagerTestCase.create_missing_file(f'{DEFAULT_STRUCTURE_ARGUMENT}/first/file0.txt')
        DatabaseManagerTestCase.create_missing_file(f'{DEFAULT_STRUCTURE_ARGUMENT}/second/file1.txt')
        DatabaseManagerTestCase.create_missing_file(f'{DEFAULT_STRUCTURE_ARGUMENT}/first/file2.txt')
        DatabaseManagerTestCase.create_missing_file(f'{DEFAULT_STRUCTURE_ARGUMENT}/fourth/fifth/file3.txt')
        os.chmod(f'{DEFAULT_STRUCTURE_ARGUMENT}/second/file1.txt', stat.S_IREAD)  # this does not cause PermissionError

    @classmethod
    def tearDownClass(cls):
        """Remove all file structures generated while testing"""
        if os.path.isdir(TEST_ROOT):
            shutil.rmtree(TEST_ROOT, onerror=cls.on_deletion_error)

    def setUp(self):
        """Gather information about directory"""
        self.data = handle_directory_file_system(DEFAULT_STRUCTURE_ARGUMENT)

    @staticmethod
    def on_deletion_error(action, name, exception):
        """Perform access rights change for a read-only file & delete it"""
        os.chmod(name, stat.S_IRWXU)
        os.remove(name)

    @staticmethod
    def create_missing_file(path):
        """Create file which location is not occupied & specified by path"""
        with open(path, 'x'):
            pass

    def test_database_writing(self):
        """Check if information is written correctly into the database"""
        database_writer = DatabaseManager(DEFAULT_DATABASE_ARGUMENT)
        database_writer.insert_information_into_database(self.data)
        connection = sqlite3.connect(DEFAULT_DATABASE_ARGUMENT)
        cursor = connection.cursor()
        cursor.execute(DATABASE_READ_DIRECTORIES)
        directories = cursor.fetchall()
        cursor.execute(DATABASE_READ_FILES)
        files = cursor.fetchall()
        connection.close()
        directory_parents = dict()
        file_parents = dict()
        directory_names = dict()
        for directory_record in directories:
            directory_parents[directory_record[DIRECTORY_RECORD_NAME_INDEX]] = \
                directory_record[DIRECTORY_RECORD_PARENT_INDEX]
            directory_names[directory_record[DIRECTORY_RECORD_ID_INDEX]] = directory_record[DIRECTORY_RECORD_NAME_INDEX]
        for file_record in files:
            file_parents[file_record[FILE_RECORD_NAME_INDEX]] = file_record[FILE_RECORD_DIRECTORY_INDEX]
        self.assertTrue(all(directory_names[directory_parents[element.name]] == element.parent.name for element in
                            self.data[1:] if isinstance(element, Directory)))  # ignoring root
        self.assertTrue(all(directory_names[file_parents[element.name]] == element.directory.name for element in
                            self.data if isinstance(element, File)))


if __name__ == '__main__':
    unittest.main()
