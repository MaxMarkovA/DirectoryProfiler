# Max Markov 01.26.2023

import sqlite3
from typing import List, Optional, Union

from information_storage import Directory, File


DIRECTORIES_TABLE_CREATION = '''
CREATE TABLE IF NOT EXISTS directories (
    id integer PRIMARY KEY,
    parent_id integer,
    name text NOT NULL,
    FOREIGN KEY(parent_id) REFERENCES directories(id)
);
'''
DIRECTORY_INSERT_COMMAND = 'INSERT OR REPLACE INTO directories(id, parent_id, name) VALUES(?, ?, ?)'

FILES_TABLE_CREATION = '''
CREATE TABLE IF NOT EXISTS files (
    id integer PRIMARY KEY,
    directory integer NOT NULL,
    name text NOT NULL,
    last_modification timestamp NOT NULL,
    access_rights text NOT NULL,
    content_hash BLOB(32) NOT NULL,
    FOREIGN KEY (directory) REFERENCES directories(id)
);
'''
FILE_GET_COMMAND = '''
SELECT * FROM files WHERE id = ?
'''
FILE_INSERT_COMMAND = '''
INSERT OR REPLACE 
INTO files(id, directory, name, last_modification, access_rights, content_hash) 
VALUES(?, ?, ?, ?, ?, ?)
'''
FILE_RECORD_LAST_MODIFICATION_INDEX = 3
FILE_RECORD_CONTENT_HASH_INDEX = 5


class DatabaseManager:
    """This class is responsible for writing file system elements information into database"""

    def __init__(self, path: str):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def insert_information_into_database(self, data: List[Union[Directory, File]]):
        """Write file system elements data into database
        NOTE: Also creates tables needed for writing & commits afterwards
        :param data: List of Directory/File objects to be written
        """
        self.cursor.execute(DIRECTORIES_TABLE_CREATION)
        self.cursor.execute(FILES_TABLE_CREATION)
        for element in data:
            self.insert_element_into_database(element)
        self.connection.commit()

    def get_file_information_from_database(self, element_id: int) -> Optional[tuple]:
        """Get element information from database
        :param element_id: ID of the desired element
        :return: Last modification date & content hash
        """
        try:
            record = self.cursor.execute(FILE_GET_COMMAND, (element_id, )).fetchone()
            if record is not None:
                return record[FILE_RECORD_LAST_MODIFICATION_INDEX], record[FILE_RECORD_CONTENT_HASH_INDEX]
            return None
        except sqlite3.OperationalError:
            return None

    def insert_element_into_database(self, element: Union[Directory, List]):
        """Write single file system element into database
        :param element: Directory/File object to be written
        """
        if isinstance(element, Directory):
            if element.id != 0:  # TODO this is caused by PermissionError
                if element.parent is None:
                    self.cursor.execute(DIRECTORY_INSERT_COMMAND, (element.id, None, element.name))
                else:
                    self.cursor.execute(DIRECTORY_INSERT_COMMAND, (element.id, element.parent.id, element.name))
        elif isinstance(element, File):
            if element.content_hash is not None:  # TODO this check is needed because of PermissionError occurrence
                self.cursor.execute(FILE_INSERT_COMMAND,
                                    (element.id, element.directory.id, element.name, element.last_modified,
                                     element.access_rights, element.content_hash))
