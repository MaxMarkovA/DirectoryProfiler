# Max Markov 01.24.2023

import messaging
from input_validator import ConsoleArgumentParser
from data_collector import handle_directory_file_system
from database_manager import DatabaseManager


PROGRAM_NAME = 'Directory Profiler'
SCRIPT_START_MESSAGE = f'{PROGRAM_NAME} has started operating'
SCRIPT_FINAL_MESSAGE = f'{PROGRAM_NAME} has finished operating'


def main():
    """Doin' Stuff..."""
    arguments, not_parsed = ConsoleArgumentParser().parse_known_args()
    messaging.messanger = messaging.MessageWriter(arguments.log, arguments.verbose)
    messaging.messanger.send_message(SCRIPT_START_MESSAGE)
    # TODO log arguments
    # TODO log mistakes with arguments
    # TODO check directory/file accessibility
    # TODO log paths to directories/files
    database_writer = DatabaseManager('sample.db')
    database_writer.insert_information_into_database(handle_directory_file_system('test_data/00'))
    messaging.messanger.send_message(SCRIPT_FINAL_MESSAGE)


if __name__ == '__main__':
    main()
