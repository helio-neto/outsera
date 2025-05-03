"""
This module provides utility functions and a factory for initializing an SQLite database and loading movie data from a CSV file.
"""

from csv import DictReader, Error
from sqlite3 import Connection, connect
from sqlite3.dbapi2 import DatabaseError
from typing import List, Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)

class DatabaseConnectionFactory:
    """
    A factory class for creating and managing SQLite database connections.
    
    This class provides a centralized method for creating database connections
    with configurable parameters and error handling.
    """
    
    @staticmethod
    def create_connection(
        check_same_thread: bool = False,
        database: str = ":memory:", 
        create_tables: bool = True
    ) -> Union[Connection, DatabaseError]:
        """
        Factory method to create a database connection.
        
        Args:
            database (str): Path to the SQLite database file. Defaults to in-memory database.
            create_tables (bool): Whether to create default tables on connection. Defaults to True.
        
        Returns:
            Connection: SQLite connection object if successful.
        
        Raises:
            DatabaseError: If the connection or table creation fails.
        """
        try:
            connection = connect(database=database, check_same_thread=check_same_thread)
            logger.info(f"Connected to database: {database}")
            
            if create_tables:
                connection.cursor().execute(
                    "CREATE TABLE IF NOT EXISTS movies (id integer primary key AUTOINCREMENT,year,title,studios,producers,winner)"
                )
            
            return connection
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise DatabaseError(e)

    @staticmethod
    def load_csv_data(
        csv_file: str = "data/Movielist.csv",
        connection: Connection = None
    ) -> None:
        """
        Loads movie data from a CSV file and inserts it into the 'movies' table in the SQLite database.

        Args:
            csv_file (str): Path to the CSV file. Defaults to 'data/Movielist.csv'.
            connection (Connection): SQLite database connection object. Must be open and valid.

        Raises:
            Error: If there is an error reading the CSV or inserting data into the database.

        Side Effects:
            Inserts records into the 'movies' table of the database.
            Logs information and errors related to the loading process.
        """
        with open(file=csv_file, mode="r", encoding="utf-8") as csv_data:
            try:
                reader = DictReader(f=csv_data, delimiter=";")
                for movie in reader:
                    connection.cursor().execute(
                        "INSERT INTO movies (year, title, studios, producers, winner) VALUES (?, ?, ?, ?, ?)",
                        (movie["year"], movie["title"], movie["studios"], movie["producers"], movie["winner"])
                    )
                logger.info(f"Loaded Movielist CSV file: {csv_file}")
            except Exception as e:
                logger.error(f"Error loading Movielist CSV file: {e}")
                raise Error(e)

    @staticmethod
    def get_db_connection() -> Connection:
        """
        Dependency function to create and manage database connections.
        
        Yields:
            Connection: An SQLite database connection.
        """
        connection = DatabaseConnectionFactory.create_connection()
        try:
            yield connection
        finally:
            connection.close()
