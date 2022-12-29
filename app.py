#!/usr/bin/env python
""" 'My Watchlist' is a mini CLI app to keep track of movies and tv shows locally.

Features:
1) Simply search online by title or id using command line: scrape information from IMDB.
2) simply add a movie or tv show using an IMDB id.
3) View upcoming movies or episodes in your wachlist. 
4) Intract with a local database (your watchlist) using sqlite3: store, view, and delete information.
5) Supports multiple users
"""

from model import MovieWatchlist, TVWatchlist
import database

__author__ = "Pejman Memar"
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Pejman Memar"
__status__ = "Development"


PROMPT = """Please select one of the following options:
1) Movies watchlist.
2) TV shows watchlist.
3) Add user to the app.
4) Exit.

Your selection: """

def open_movie_watchlist(): # Movie watchlist menu
    movie_watchlist = MovieWatchlist()
    movie_watchlist.menu()

def open_tv_watchlist(): # TV watchlist menu
    tv_watchlist = TVWatchlist()
    tv_watchlist.menu()

def add_user(): # add user to the app
    username = input("\nUsername: ")
    try:
        database.add_user(username)
    except:
        print(f"\n{username} is already existed. Try a different username.\n")

MENU_OPTIONS = {
"1": open_movie_watchlist,
"2": open_tv_watchlist,
"3": add_user
}

def menu():
    database.create_tables()
    while (selection := input(PROMPT)) != "4":
        try:
            MENU_OPTIONS[selection]()

        except KeyError:
            print("\nInvalid input selected. Please try again.\n")


if __name__ == "__main__":
    print("Welcome to your watchlist app!\n")
    menu()

