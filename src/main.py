###############################
# Golden Raspberry Awards API #
###############################
import logging

from fastapi import FastAPI

from sqlite3 import connect

from database.sqlite_database import load_csv_data

from services.analysis import analyze_movie_winners

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/golden_raspberry_app.log', level=logging.INFO)

app = FastAPI()

memory_connection = connect(database=":memory:",check_same_thread=False)
memory_connection.cursor().execute(
    "CREATE TABLE IF NOT EXISTS movies (id integer primary key AUTOINCREMENT,year integer,title,studios,producers,winner)"
)


@app.on_event("startup")
def on_startup():
    """
    FastAPI startup event handler.
    Loads movie data from CSV into the in-memory SQLite database on application startup.
    """
    load_csv_data(connection=memory_connection)


@app.get("/movies")
def get_all_movies():
    """
    Returns all movies in the database.
    
    Returns:
        list: A list of all movie records as tuples.
    """
    movie_data = memory_connection.cursor().execute("SELECT * FROM movies").fetchall()
    return movie_data


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    """
    Returns a single movie by its ID.
    
    Args:
        movie_id (int): The ID of the movie to retrieve.
    
    Returns:
        tuple or None: The movie record as a tuple, or None if not found.
    """
    movie = memory_connection.cursor().execute("SELECT * FROM movies WHERE id = ?", (movie_id,)).fetchone()
    return movie


@app.get("/movie/winners")
def get_movie_winners():
    """
    Returns analysis of movie winners.

    Returns:
        dict: A dictionary containing two lists: 'min' and 'max' time that a producer has won the Golden Raspberry Awards.
    """
    raw_winner_list = memory_connection.cursor().execute(
        "SELECT year, producers FROM movies WHERE winner ='yes'"
    ).fetchall()
    winner_list = analyze_movie_winners(raw_winner_list)
    return winner_list
