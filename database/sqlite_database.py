from csv import DictReader, Error

from sqlite3 import Connection, connect
from sqlite3.dbapi2 import DatabaseError

from typing import List, Dict

import logging

logger = logging.getLogger(__name__)


def start_database(database: str = ":memory:") -> (Connection | DatabaseError):
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
) -> (List[Dict[str, str]] | Error):
    with open(file=csv_file, mode="r", encoding="utf-8") as csv_data:
        try:
            reader = DictReader(f=csv_data, delimiter=";")
            for movie in reader:
                connection.cursor().execute(
                    "INSERT INTO movies (year, title, studios, producers, winner) VALUES (?, ?, ?, ?, ?)",
                    (movie["year"], movie["title"], movie["studios"], movie["producers"], movie["winner"])
                )
            logger.info(f"Loaded Movielist csv file: {csv_file}")
            return list(reader)
        except Exception as e:
            logger.error(f"Error loading Movielist csv file: {e}")
            raise Error(e)
