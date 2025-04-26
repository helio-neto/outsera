"""
This module provides utility functions for initializing an SQLite database and loading movie data from a CSV file into the database.
"""

from csv import DictReader, Error

from sqlite3 import Connection, connect
from sqlite3.dbapi2 import DatabaseError

from typing import List, Dict

import logging

logger = logging.getLogger(__name__)


def start_database(database: str = ":memory:") -> (Connection | DatabaseError):
    """
    Initialize and connect to an SQLite database. Creates a 'movies' table if it does not exist.

    Args:
        database (str): Path to the SQLite database file. Defaults to in-memory database.

    Returns:
        Connection: SQLite connection object if successful.

    Raises:
        DatabaseError: If the connection or table creation fails.
    """
    try:
        connection = connect(database)
        print(f"Connected to database: {database}")
        connection.cursor().execute(
            "CREATE TABLE IF NOT EXISTS movies (id integer primary key AUTOINCREMENT,year,title,studios,producers,winner)"
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise DatabaseError(e)


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
            logger.info(f"Loaded Movielist csv file: {csv_file}")
        except Exception as e:
            logger.error(f"Error loading Movielist csv file: {e}")
            raise Error(e)
