#!/usr/bin/env python
"""
Scrape movies and tv shows information from IMDB.

Typical usage example:
> search = Search(tv_show=False)
> search.search_by_title("avengers")
> search.search_by_id("16358384")

To interact with users:
> search = Search(tv_show=False)
> search.prompt_search_by_title()
> search.prompt_search_by_id()
"""
from typing import List
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests

class Search:
    """
    Search online using title or id via scraping information from IMDB.

    Attributes:
    tv_show: a boolean flag to determine whether search for movies or tv shows
    """
    def __init__(self, tv_show=False):
        """
        Init Search class with tv_show flag.
        """
        self.tv_show = tv_show

    def __get_response(self, url: str):
        """
        Get response from the web.

        Args:
        url (str): input web address

        return:
        requests.model
        """
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()

        except requests.ConnectionError as e:
            print(f"Connection Error. Make sure you are connected to Internet.\n{e}")
        except requests.Timeout as e:
            print(f"Timeout Error: {e}")
        except requests.RequestException as e:
            print(f"General Error: {e}")
        except requests.TooManyRedirects as e:
            print(f"Too many redirects: {e}")
        except requests.HTTPError as e:
            print(f"HTTP Error: {e}")
        except KeyboardInterrupt:
            print("Keyboard interrupt: program is closed.")

        return response

    def search_by_title(self, title: str) -> List:
        """
        Find relevent movies or tv shows from IMDB based on the entered title.

        Args:
        title (str): (partial) title of a movie or tv show

        Return:
        list: list of searched items 
        """
        url = f"https://www.imdb.com/find/?q={title}&s=tt"
        response = self.__get_response(url)
        content = BeautifulSoup(response.text, 'html.parser')

        root = content.findAll('div', class_='ipc-metadata-list-summary-item__tc')
        if root:
            search_results = []
            for items in root:
                imdb_id = items.find('a').attrs['href'].split('/')[2][2:]
                title = items.find('a').text
                search_results.append([imdb_id, title]+[a.text for a in items.findAll('li')])
            
            return search_results
        else:
            raise Exception("Unable to parse the information. Probably the HTML elements have been changed. Please report this issue on Github.")

        
    def __clean_search_by_title_results(self, search_results: List) -> pd.DataFrame:
        final_results = []
        """
        Clean output data of search_by_title function.

        Args:
        search_results (list): output of search_by_title function

        Return:
        DataFrame: cleaned data
        """
        for result in search_results:
            if len(result) == 7:
                final_results.append([result[0], result[1], result[2], result[-1], result[-2]])
            elif len(result) == 6:
                final_results.append([result[0], result[1], result[2], result[-1], ''])
            elif len(result) == 5:
                final_results.append(result)
            elif len(result) == 4:
                final_results.append([result[0], result[1], result[2], 'Movie', result[3]])
            elif len(result) in [2,3]:
                final_results.append([result[0], result[1], 'NA', 'NA', 'NA'])
            elif len(result) == 1:
                final_results.append([result[0], 'NA', 'NA', 'NA', 'NA'])
            else:
                raise Exception("Unable to parse the information. Probably the HTML elements have been changed. Please report this issue on Github.")

        results = pd.DataFrame(final_results)
        results.columns = ["imdb_id", "title", "release_date", "type", "cast"]
        return results


    def search_by_id(self, imdb_id: str) -> pd.DataFrame:
        """
        Find relevent movies or tv shows from IMDB based on the entered ID.

        Args:
        imdb_id (str): IMDB id

        Return:
        list: searched item
        """
        url = f'https://www.imdb.com/title/tt{imdb_id}/'
        response = self.__get_response(url)
        content = BeautifulSoup(response.text, 'html.parser')

        title = content.findAll('h1', attrs={'data-testid':'hero-title-block__title'})[0].text

        description = content.findAll('span', attrs={'data-testid':'plot-xl'})[0].text

        root = content.findAll('ul', attrs={'data-testid':'hero-title-block__metadata'})[0].findAll('li')

        if title and description and root:
            try:
                rating = content.findAll('div', attrs={'data-testid':'hero-rating-bar__aggregate-rating__score'})[0].text
            except:
                rating = 'NA'

            if len(root) == 4:
                type_ = root[0].text
                release_date = root[1].find('span').text
                runtime = root[-1].text

            elif len(root) == 3:
                type_ = 'Movie'
                release_date = root[0].find('span').text
                runtime = root[-1].text

            elif len(root) == 2:
                type_ = root[0].text
                release_date = root[1].find('span').text
                runtime = 'NA'

            elif len(root) == 1:
                type_ = 'Movie'
                release_date = root[0].find('span').text
                runtime = 'NA'
            
            else:
                raise Exception("Unable to parse the information. Please report this issue on Github.")

            final_results = [imdb_id, title, release_date, type_, rating, runtime, description]
            results = pd.DataFrame(final_results)
            results.index = ["imdb_id", "title", "release_date", "type", "rating", "runtime", "discription"]
            return results

        else:
            raise Exception("Unable to parse the information. Probably the HTML elements have been changed. Please report this issue on Github.")

        
    def upcoming_episodes(self, imdb_id: str) -> List:
        """
        Find upcoming episodes from IMDB based on the entered ID.

        Args:
        imdb_id (str): IMDB id

        Return:
        list: searched items
        """
        url = f'https://www.imdb.com/title/tt{imdb_id}/episodes/'
        response = self.__get_response(url)
        content = BeautifulSoup(response.text, 'html.parser')

        movie_title = content.findAll('h3', attrs={'itemprop':'name'})[0].find('a').text.strip()

        selected_season = content.findAll('option', attrs={'selected':'selected'})[0].text.strip()
        seasons = content.findAll('select', attrs={'id':'bySeason'})[0].text
        all_seasons = [season for season in seasons if season.isdigit()]

        if movie_title and selected_season.isdigit() and int(selected_season) < 70:
            if selected_season != all_seasons[-1]:
                url_1 = f"https://www.imdb.com/title/tt{imdb_id}/episodes?season={selected_season}"
                url_2 = f"https://www.imdb.com/title/tt{imdb_id}/episodes?season={all_seasons[-1]}"

                results = self.scrape_episodes(url_1, upcoming=True) +\
                          self.scrape_episodes(url_2, upcoming=True)
            
            else:
                results = self.scrape_episodes(url, upcoming=True)

            if results:
                search_results = pd.DataFrame(results)
                search_results.columns = ["title", "season", "episode", "airdate"]
                return [search_results, movie_title]
            
            else:
                results = f"Found no upcoming episodes for {movie_title}."
                return [results, movie_title]

        else:
            raise Exception("Unable to parse the information. Probably the HTML elements have been changed. Please report this issue on Github.")


    def scrape_episodes(self, url: str, upcoming: bool = False) -> List:
        """
        Find all episodes from IMDB based on the entered ID.

        Args:
        url (str): url of tv show's episodes guide

        Return:
        list: searched items
        """
        response = self.__get_response(url)  
        content = BeautifulSoup(response.text, 'html.parser')
        episodes = content.find_all('div', class_='info')
        season = content.findAll('option', attrs={'selected':'selected'})[0].text.strip()
        results = []
        for episode in episodes:
            airdate = episode.find('div', class_='airdate').text.strip()
            if airdate and upcoming:
                episode_timestamp = datetime.strptime(airdate, "%d %b. %Y").timestamp()
                now_timestamp = datetime.now().timestamp()
                if episode_timestamp >= now_timestamp:
                    title = episode.a['title']
                    episode_num = episode.meta['content']
                    results.append([title, season, episode_num, airdate])

            elif airdate and not upcoming:
                    title = episode.a['title']
                    episode_num = episode.meta['content']
                    results.append([title, season, episode_num, airdate])
                
        return results


    def prompt_search_by_title(self):
        """
        Interact with user for the search_by_title function
        """
        try:
            title = input("Enter a partial title: ")
            search_results = self.search_by_title(title)
            results = self.__clean_search_by_title_results(search_results)
            if self.tv_show:
                results = results[results['type'].str.startswith("TV")]
                print("\n-- Search Results --\n")
                print(results.head(25).to_string(index=False))
                print("\n-- End --\n")
            else:
                print("\n-- Search Results --\n")
                results = results[~results['type'].str.startswith("TV")]
                print(results.head(25).to_string(index=False))
                print("\n-- End --\n")
        except:
            print("\nError: Invalid input. Please try again.\n")
    

    def prompt_search_by_id(self) -> pd.DataFrame:
        """
        Interact with user for the search_by_id function
        """
        try:
            imdb_id = input("Enter an IMDB ID (only numbers): ")
            results = self.search_by_id(imdb_id).T

            if self.tv_show and not results['type'][0].startswith("TV"):
                print("\nThis is a movie. You can only search for tv shows here.\n")
                return None
            elif not self.tv_show and results['type'][0].startswith("TV"):
                print("\nThis is a tv show. You can only search for movies here.\n")
                return None
            else:
                print("\n-- Search Results --")
                print(f"IMDB ID: {results.imdb_id[0]}")
                print(f"Title: {results.title[0]}")
                print(f"Release Date: {results.release_date[0]}")
                print(f"Rating: {results.rating[0]}")
                print(f"Runtime: {results.runtime[0]}")
                print(f"Type: {results.type[0]}")
                print(f"Description: {results.discription[0]}")
                print("-- End --\n")

            return results
        except:
            print("\nError: Invalid ID. Please try again.\n")
