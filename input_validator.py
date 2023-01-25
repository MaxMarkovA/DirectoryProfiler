# Max Markov 01.25.2023

from argparse import ArgumentParser


SCRIPT_NAME = 'directory_profiler.py'
PROGRAM_DESCRIPTION = 'Gather information about directory & write it into database'


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
