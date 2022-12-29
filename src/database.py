#!/usr/bin/env python
"""
Create a local database and interact with it.

This database consists of 4 tables:
1) movies: to keep tarck of movies.
2) shows: to keep track of tv shows.
3) users: to keep track of users.
4) watched: to keep track of watched movies (only for the movie wachlist).
"""

from typing import Tuple
import datetime
import sqlite3

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies(
    id INTEGER PRIMARY KEY,
    imdb_id TEXT,
    title TEXT,
    release_date_timestamp REAL,
    rating TEXT,
    type_ TEXT,
    runtime TEXT,
    description TEXT
    );"""

# seperate table for future extentions
CREATE_SHOWS_TABLE = """CREATE TABLE IF NOT EXISTS shows(
    id INTEGER PRIMARY KEY,
    imdb_id TEXT,
    title TEXT,
    release_date_timestamp REAL,
    rating TEXT,
    type_ TEXT,
    runtime TEXT,
    description TEXT
    );"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    unique (username)
    );"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched(
    user_username TEXT,
    movie_id INTEGER,
    unique (user_username, movie_id),
    FOREIGN KEY(user_username) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
    );"""

INSERT_USER = "INSERT INTO users (username) VALUES (?);"

INSERT_MOVIES = "INSERT INTO movies (imdb_id, title, release_date_timestamp, rating, type_, runtime, description) VALUES (?,?,?,?,?,?,?);"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_date_timestamp > ?;"
SELECT_WATCHED_MOVIES = """SELECT DISTINCT movies.* FROM movies
JOIN watched ON movies.id = watched.movie_id
JOIN users ON users.username = watched.user_username
WHERE users.username = ?;"""
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES (?,?);"
SET_WATCHED_MOVIE = "UPDATE movies SET watched = 1 WHERE title = ?;"
CREATE_RELEASE_INDEX = "CREATE INDEX IF NOT EXISTS idx_movies_release ON movies(release_date_timestamp);"


DELETE = "DELETE FROM {table_name} WHERE id = ?;"
SELECT_ALL = "SELECT * FROM {table_name};"
SEARCH = "SELECT * FROM {table_name} WHERE title LIKE ?;"
#--------------------------------------

INSERT_SHOWS = "INSERT INTO shows (imdb_id, title, release_date_timestamp, rating, type_, runtime, description) VALUES (?,?,?,?,?,?,?);"
SELECT_IMDB_ID_SHOWS = "SELECT imdb_id FROM shows;"
#-------------------------------------

connection = sqlite3.connect("data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_SHOWS_TABLE)
        connection.execute(CREATE_USERS_TABLE)
        connection.execute(CREATE_WATCHED_TABLE)
        connection.execute(CREATE_RELEASE_INDEX)

def add_user(username: str):
    with connection:
        connection.execute(INSERT_USER, (username,))

# -- Movies --

def add_movie(imdb_id: str, title: str, release_date_timestamp: int, rating: str, type_: str, runtime: str, description: str):
    with connection:
        connection.execute(INSERT_MOVIES, (imdb_id, title, release_date_timestamp, rating, type_, runtime, description))

def get_movies(upcoming: bool = False) -> Tuple:
    with connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL.format(table_name='movies'))
        return cursor.fetchall()

def watch_movie(username: str, movie_id: str):
    with connection:
        try:
            connection.execute(INSERT_WATCHED_MOVIE, (username, movie_id))
        except:
            print(f"\n{movie_id} is already in the watched movies.\n")

def get_watched_movies(username: str) -> Tuple:
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (username,))
        return cursor.fetchall()

def search_movies(search_term: str) -> Tuple:
    with connection:
        cursor = connection.cursor()
        cursor.execute(SEARCH.format(table_name='movies'), (f"%{search_term}%",))
        return cursor.fetchall()

def delete_movie(movie_id: str):
    with connection:
        connection.execute(DELETE.format(table_name='movies'), (movie_id,))
        
# -- TV Shows --

def add_show(imdb_id: str, title: str, release_date_timestamp: str, rating: str, type_: str, runtime: str, description: str):
    with connection:
        connection.execute(INSERT_SHOWS, (imdb_id, title, release_date_timestamp, rating, type_, runtime, description))

def get_imdb_id() -> Tuple:
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_IMDB_ID_SHOWS)
        return cursor.fetchall()

def get_shows() -> Tuple:
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ALL.format(table_name='shows'))
        return cursor.fetchall()

def search_shows(search_term: str) -> Tuple:
    with connection:
        cursor = connection.cursor()
        cursor.execute(SEARCH.format(table_name='shows'), (f"%{search_term}%",))
        return cursor.fetchall()

def delete_show(movie_id: str) -> Tuple:
    with connection:
        connection.execute(DELETE.format(table_name='shows'), (movie_id,))
