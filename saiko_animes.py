import requests
from lxml import html
import re

import constants
from custom_errors import NotFoundError


class SaikoAnime():
    def __init__(self, anime_url: str) -> None:
        self.anime_url = anime_url
        self.headers = {
            'cookie': 'copy and paste here',
            'origin': 'https://saikoanimes.net'
        }
        self.html_tree = None
        self.anime_title = None
        self.showing_status = None
        self.cover_url = None
        self.season_urls = []
        self.episodes = []
        
    def get_html_tree(self) -> None:
        anime_page = requests.get(self.anime_url, headers=self.headers)
        self.html_tree = html.fromstring(anime_page.content)
    
    def get_anime_title(self) -> None:
        search_result = self.html_tree.xpath(constants.ANIME_TITLE_XPATH)

        if search_result:
            title = search_result[0]
            title = re.sub(constants.REGEX_REMOVE_LAST_SPACE_AND_TABULATION, '-', title)
            title = re.sub(constants.REGEX_REMOVE_SPECIAL_CHARACTERS, '', title)
            self.anime_title = title

        else:
            raise NotFoundError(message=f"{self.anime_url} - Title not found.")  

    def get_display_status(self) -> None:
        search_result = self.html_tree.xpath(constants.ANIME_DISPLAY_STATUS_XPATH)
        
        if search_result:
            self.showing_status =  search_result[0]
        
        else:
            raise NotFoundError(message=f"{self.anime_url} - Error on get display status.")
    
    def get_cover_url(self) -> None:
        search_result = self.html_tree.xpath(constants.ANIME_COVER_XPATH)
        
        if search_result:
            self.cover_url = search_result[0].get('src')
            
        else:
            raise NotFoundError(message=f"{self.anime_url} - Error on get anime cover.")

    def get_season_urls(self) -> None:
        for season in range(1, 20):
            result_search = self.html_tree.xpath(constants.ANIME_SEASONS_XPATH_V1.format(season))
            if not result_search:
                result_search = self.html_tree.xpath(constants.ANIME_SEASONS_XPATH_V2.format(season))
            
            if result_search:
                self.season_urls.append(result_search[0].get('href'))
        
        if not self.season_urls:
            raise NotFoundError(message=f"{self.anime_url} - Error on get anime seasons.")
    
    def get_episodes_from_seasons(self) -> None:
        try:
            for season, episodes_url in enumerate(self.season_urls):
                season += 1
                anime_hash = episodes_url.split('/')
                anime_hash = anime_hash[len(anime_hash) - 1].replace("baixar?=", "").replace("baixarr?=", "")
                season_page = requests.get(constants.ANIME_EPISODE_INFORMATIONS_URL.format(anime_hash), headers=self.headers)
                season_page_html_tree = html.fromstring(season_page.content)
                search_episodes_result = season_page_html_tree.xpath(constants.EPISODES_XPATH)
                self.episodes = self.get_episodes_from_session(search_episodes_result, season)
                
        except:
            raise NotFoundError(message="Episodes url not found")

    def get_episodes_from_session(self, search_episodes_result, season):
        episodes = []
        
        index_1080 = None
        for index, episode in enumerate(search_episodes_result):
            url = episode.get('data-url')
            name = episode.xpath('.//div')[0].xpath('.//i')[0].tail
            if '1080' in name and 'folder' in url:
                index_1080 = index
        
        if index_1080:
            search_episodes_result = [search_episodes_result[index_1080]]
            
        for episode in search_episodes_result:
            url = episode.get('data-url')
            name = episode.xpath('.//div')[0].xpath('.//i')[0].tail
            
            if 'folder' in url:
                anime_page = requests.get(url, headers=self.headers)
                html_tree = html.fromstring(anime_page.content)
                search_episodes_result = html_tree.xpath(constants.EPISODES_XPATH)
                episodes += self.get_episodes_from_session(search_episodes_result, season)     
            
            if '.' in name:
                episodes.append(
                    {
                        "anime_title": self.anime_title,
                        "season": f"S{season}",
                        "url": url,
                        "episode_name": name
                    }
                )
        
        return episodes
