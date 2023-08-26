from custom_errors import CustomError
from downloader import Downloader
from saiko_animes import SaikoAnime
import sys


if __name__ == '__main__':
    try:
        anime = SaikoAnime(
            anime_url=sys.argv[1]
        )
        anime.get_html_tree()
        anime.get_anime_title()
        anime.get_display_status()
        anime.get_cover_url()
        anime.get_season_urls()
        anime.get_episodes_from_seasons()
        
        downloader = Downloader(
            anime_title=anime.anime_title,
            cover_url=anime.cover_url,
            showing_status=anime.showing_status
        )
        
        downloader.create_anime_folder()
        downloader.download_cover()
        
        for episode in anime.episodes:
            downloader.download_episode_from_saiko_drive(episode)
    
    except CustomError as ex:
        print(ex.message)
        
    except Exception as ex:
        print(ex)
