import requests
import os
from tqdm import tqdm


class Downloader():
    def __init__(self, anime_title: str, cover_url: str, showing_status: str) -> None:
        self.anime_title = anime_title
        self.cover_url = cover_url
        self.showing_status = showing_status
        self.download_base_path = './downloads'
    
    def create_anime_folder(self):
        if not os.path.exists(f'{self.download_base_path}'):
            os.mkdir(f'{self.download_base_path}')
            
        if not os.path.exists(f'{self.download_base_path}/{self.anime_title}'):
            os.mkdir(f'{self.download_base_path}/{self.anime_title}')

    def download_cover(self) -> None:
        response = requests.get(self.cover_url)
        with open(f'{self.download_base_path}/{self.anime_title}/cover.jpg', 'wb') as file:
            for data in response.iter_content(1024 * 1024):
                file.write(data)
    
    def download_episode_from_saiko_drive(self, episode_information: str) -> None:
        folder_path = f'{self.download_base_path}/{self.anime_title}/{episode_information["season"]}'
        archive_path = f'{self.download_base_path}/{self.anime_title}/{episode_information["season"]}/{episode_information["episode_name"]}'

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        
        if not os.path.exists(archive_path):
            video_response = requests.get(episode_information.get('url'), stream=True)
            
            if self.showing_status == 'Completo':
                print(f'\033[1;33;40m anime completo {episode_information["episode_name"]}')
            
            else:
                print(f'\033[0;34m anime em exibição {episode_information["episode_name"]}')
                
            total_size_in_bytes= int(video_response.headers.get('content-length', 0))
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
            
            with open(archive_path, 'wb') as file:
                for data in video_response.iter_content(1024 * 1024):
                    progress_bar.update(len(data))
                    file.write(data)
                    
            progress_bar.close()
            
        else:
            print(f"\033[1;32;40m{episode_information['episode_name']} already exists")
