
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/) [![Issue](https://img.shields.io/github/issues/pejmanmemar/MyWatchlist.svg)](https://img.shields.io/github/issues/pejmanmemar/MyWatchlist.svg)

# My Watchlist
**My Watchlist** is a mini CLI app to keep track of movies and TV shows locally.

Features:
- Simply search online by title or ID (the app will scrape information from IMDB).
- Simply add a movie or TV show using an IMDB ID.
- View upcoming movies or episodes in your watchlist. 
- Interact with a local database (your watchlist) using sqlite3: store, view, and delete information.
- Supports multiple users

# Instruction
1. Install the required packages mentioned in the requirements.txt file.
2. Make sure you have Python3.8 installed on your system.
3. Open terminal and run:
```
> cd src/
> python3.8 app.py
```
# Demo

- Search for a movie and add it to the movie watchlist:

![screen-gif](./demo/part_1.gif)

- Watched movies for a specific user:

![screen-gif](./demo/part_2.gif)

- List of TV shows and upcoming episodes:

![screen-gif](./demo/part_3.gif)
