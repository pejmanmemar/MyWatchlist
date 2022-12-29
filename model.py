#!/usr/bin/env python
""" 
Designed model to interact with search and database modules (the building block of app.py). 
"""
import sys
from typing import Tuple
from search import Search
import pandas as pd
import datetime
sys.path.insert(0,'..')
import database


class MovieWatchlistMenu:
    """ Movie watchlist menu options """
    ADD_TO_WATCHLIST = '1'
    SEARCH = '2'
    VIEW_ALL_MOVIES = '3'
    VIEW_WATCHED_MOVIES = '4'
    VIEW_UPCOMING_MOVIES = '5'
    WATCH = '6'
    DELETE = '7'
    EXIT = '8'

class TVWatchlistMenu:
    """ TV watchlist menu options """
    ADD_TO_WATCHLIST = '1'
    SEARCH = '2'
    VIEW_ALL_SHOWS = '3'
    VIEW_UPCOMING_EPISODES = '4'
    DELETE = '5'
    EXIT = '6'

class AddToWatchlistMenu:
    """ Add to watchlist menu options """
    SEARCH_BY_TITLE = '1'
    ADD_TO_WATCHLIST = '2'
    EXIT = '3'


#------------------------------

class MovieWatchlist:
    """Movie watchlist class"""
    def __init__(self):
        pass

    def menu(self):
        MOVIE_WATCHLIST_PROMPT = """What would you like to do?
1) Add to wachlist. 
2) Search (local database only).
3) View all movies in your watchlist.
4) View watched movies.
5) View upcoming movies in your watchlist.
6) Watch a movie from your watchlist.
7) Delete a movie.
8) Go back.

Your selection: """
        while (user_input := input(MOVIE_WATCHLIST_PROMPT)) != MovieWatchlistMenu.EXIT:
            user_input == '1'
            if user_input == MovieWatchlistMenu.ADD_TO_WATCHLIST:
                AddToWatchlist().menu()
            elif user_input == MovieWatchlistMenu.SEARCH:
                self.search_locally()
            elif user_input == MovieWatchlistMenu.VIEW_ALL_MOVIES:
                self.view_all_movies()
            elif user_input == MovieWatchlistMenu.VIEW_WATCHED_MOVIES:
                self.view_watched_movies()                        
            elif user_input == MovieWatchlistMenu.VIEW_UPCOMING_MOVIES:
                self.view_upcoming_movies()
            elif user_input == MovieWatchlistMenu.WATCH:
                self.__watch_movie()
            elif user_input == MovieWatchlistMenu.DELETE:
                self.__delete_movie()                                    
            else:
               print("\nInvalid input, please try again!\n")

    def __print_movie_list(self, heading: str, movies: Tuple):
        print(f"\n-- {heading} Movies --")
        for id_, imdb_id, title, release_date, rating, _, runtime, _ in movies:
            movie_date = datetime.datetime.fromtimestamp(release_date)
            human_date = movie_date.strftime("%Y")
            print(f"{id_} (IMDB ID: {imdb_id!r}): {title!r} (on {human_date}) - {rating} - {runtime}")
        print("-- End --\n")   

    def search_locally(self):
        search_term = input("Enter the partial movie title: ")
        movies = database.search_movies(search_term)
        if movies:
            self.__print_movie_list("Found", movies)
        else:
            print("\nFound no movies for that search term!\n")

    def view_all_movies(self):
        movies = database.get_movies()
        self.__print_movie_list('All', movies)

    def view_watched_movies(self):
        username = input("Username: ")
        movies = database.get_watched_movies(username)
        if movies:
            self.__print_movie_list("Watched", movies)
        else:
            print(f"\n{username} has watched no movies yet!\n") 

    def view_upcoming_movies(self):
        movies = database.get_movies(True)
        if movies:
            self.__print_movie_list("Upcoming", movies)
        else:
            print(f"\nThere are no upcoming movies in the watchlist!\n")  

    def __watch_movie(self):
        username = input("Username: ")
        movie_id = input("Movie ID (NOT IMDB ID): ")
        database.watch_movie(username, movie_id)
    
    def __delete_movie(self):
        print("\nWARNING: this will delete the movie for all users.\n")
        imdb_id = input("Movie ID (NOT IMDB ID): ")
        user_input = input('Are you sure you want to delete this movie (y/N)? ').lower()
        if user_input == 'y':
            database.delete_movie(imdb_id)
            print(f"\n-- Selected movie is deleted from your database --\n\n")

#------------------------------

class TVWatchlist:
    """TV watchlist class"""
    def __init__(self):
        pass

    def menu(self):
        TV_WATCHLIST_PROMPT = """What would you like to do?
1) Add tv show. 
2) Search (local database only).
3) View all TV shows in your watchlist.
4) View upcoming episodes.
5) Delete tv show.
6) Go back.

Your selection: """

        while (user_input := input(TV_WATCHLIST_PROMPT)) != TVWatchlistMenu.EXIT:
            user_input == '1'
            if user_input == TVWatchlistMenu.ADD_TO_WATCHLIST:
                AddToWatchlist(tv_show=True).menu()
            elif user_input == TVWatchlistMenu.SEARCH:
                self.search_locally()
            elif user_input == TVWatchlistMenu.VIEW_ALL_SHOWS:
                self.view_all_shows()                    
            elif user_input == TVWatchlistMenu.VIEW_UPCOMING_EPISODES:
                self.view_upcoming_episodes()
            elif user_input == TVWatchlistMenu.DELETE:
                self.__delete_show()                                    
            else:
                print("\nInvalid input, please try again!\n")

    def search_locally(self):
        search_term = input("Enter the partial show title: ")
        shows = database.search_shows(search_term)
        if shows:
            self.__print_show_list("Found", shows)
        else:
            print("\nFound no tv shows for that search term!\n")

    def __print_show_list(self, heading: str, movies: Tuple):
        print(f"\n-- {heading} TV Shows --")
        for id_, imdb_id, title, release_date, rating, _, runtime, _ in movies:
            print(f"{id_} (IMDB ID: {imdb_id!r}): {title!r} ({release_date}) - {rating} - {runtime}")
        print("-- End --\n")   

    def view_all_shows(self):
        shows = database.get_shows()
        self.__print_show_list('All', shows)
    
    def view_upcoming_episodes(self):
        imdb_ids = database.get_imdb_id()
        search = Search()
        for id_ in imdb_ids:
            results, title = search.upcoming_episodes(id_[0])
            if isinstance(results, pd.DataFrame):
                print(f"\n-- {title} --")
                print(results.to_string(index=False))
                print("-------- \n")
            else:
                print(results)
                print("-------- \n")
    
    def __delete_show(self):
        print("\nWARNING: this will delete the tv show for all users.\n")
        imdb_id = input("TV Show ID (NOT IMDB ID): ")
        user_input = input('Are you sure you want to delete this tv show (y/N)? ').lower()
        if user_input == 'y':
            database.delete_show(imdb_id)
            print(f"\n-- Selected tv show is deleted from your database --\n\n")

#------------------------------

class AddToWatchlist:
    """
    Add to watchlist class
    
    Attributes:
    tv_show: a boolean flag to determine whether search for movies or tv shows
    """
    def __init__(self, tv_show=False):
        self.tv_show = tv_show

    def menu(self):
        ADD_TO_WATCHLIST_PROMPT = """Please select one of the following options:
1) Search online by title. 
2) Add to watchlist using an IMDB id (find it using option '1').
3) Go back.

Your selection: """
        while (user_input := input(ADD_TO_WATCHLIST_PROMPT)) != AddToWatchlistMenu.EXIT:
            user_input == '1'
            if user_input == AddToWatchlistMenu.SEARCH_BY_TITLE:
                self.search_by_title()
            elif user_input == AddToWatchlistMenu.ADD_TO_WATCHLIST:
                self.__add_to_wachlist()
            else:
               print("\nInvalid input, please try again!\n")

    def search_by_title(self):
        search = Search(self.tv_show)
        return search.prompt_search_by_title()

    def search_by_id(self):
        search = Search(self.tv_show)
        print("\nWARNING: you need an IMDB id here. Copy it from the output of option '1'.\n")
        return search.prompt_search_by_id()

    def __add_to_wachlist(self):
        results = self.search_by_id()
        if results is not None:
            user_input = input('Would you like to add this to your watchlist (Y/n)? ').lower()
            if user_input != 'n':
                if self.tv_show:
                    release_date = results.release_date[0]
                    database.add_show(  results.imdb_id[0],
                                        results.title[0],
                                        release_date,
                                        results.rating[0],
                                        results.type[0],
                                        results.runtime[0],
                                        results.discription[0])
                    
                else:
                    date_time = results.release_date[0]
                    release_date = datetime.datetime.strptime(date_time, "%Y").timestamp()
                    database.add_movie( results.imdb_id[0],
                                        results.title[0],
                                        release_date,
                                        results.rating[0],
                                        results.type[0],
                                        results.runtime[0],
                                        results.discription[0])
                print(f"\n-- {results.title[0]!r} is added to your watchlist --\n\n")









