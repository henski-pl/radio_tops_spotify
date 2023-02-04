import json
from typing import Union
from .song import Song
from .spotify import create_playlist, remove_playlist, add_songs_to_playlist, remove_songs_from_playlist, get_playlist_items
from .package_logging import logger
from .config import settings

PLAYLIST_IDS = {}


class Playlist:

    def __init__(self, name: str, desc: str, public: bool):
        self.name = name
        self.desc = desc
        self.public = public
        self.spotify_id = self.__create_playlist()
        if self.spotify_id is not None:
            self.songs = set(get_playlist_items(self.spotify_id))
        else:
            self.songs = set()

    def __create_playlist(self) -> str:
        global PLAYLIST_IDS

        spotify_id = self.__read_playlist_id_from_file()

        if spotify_id is not None:
            self.spotify_id = spotify_id
            return self.spotify_id

        spotify_id = create_playlist(self.name, self.desc, self.public)

        if spotify_id is not None:
            PLAYLIST_IDS[self.name] = spotify_id
            self.__write_playlist_id_to_file()
            self.spotify_id = spotify_id
            return self.spotify_id

    def __read_playlist_id_from_file(self) -> Union[None, str]:
        global PLAYLIST_IDS

        if self.name in PLAYLIST_IDS.keys():
            return PLAYLIST_IDS[self.name]

        try:
            with open(settings.playlist_ids_file, 'r', encoding='utf-8') as json_file:
                playlist_ids = json.load(json_file)
                PLAYLIST_IDS = playlist_ids
                if self.name in PLAYLIST_IDS.keys():
                    return PLAYLIST_IDS[self.name]
        except FileNotFoundError as e:
            logger.debug(f'File {settings.playlist_ids_file} not found')

        return None

    @staticmethod
    def __write_playlist_id_to_file() -> None:
        global PLAYLIST_IDS

        logger.info(f'Writing playlist ids to file {settings.playlist_ids_file}')
        with open(settings.playlist_ids_file, 'w', encoding='utf-8') as json_file:
            json.dump(PLAYLIST_IDS, json_file, ensure_ascii=False, indent=4)

    def remove_playlist(self) -> None:
        try:
            if self.spotify_id is not None:
                remove_playlist(self.spotify_id)
        except Exception as e:
            logger.error(f'Failed to remove playlist {self.name}')
        else:
            global PLAYLIST_IDS
            del PLAYLIST_IDS[self.name]

    def add_songs(self, songs: Union[list[str], list[Song]]) -> None:
        songs_track_ids = []

        for song in songs:
            if song.track_id is not None:
                songs_track_ids.append(song.track_id)

        songs_to_add = set(songs_track_ids).difference(self.songs)
        logger.debug(f'Items that will be added to playlist {self.name}: {songs_to_add}')

        try:
            add_songs_to_playlist(songs_to_add, self.spotify_id)
        except Exception as e:
            logger.error(f'Failed to add songs to playlist {self.name}')
            logger.exception(e)
        else:
            logger.info(f'Succesfully added songs to playlist {self.name}')
            self.songs.update(set(songs_to_add))

    def remove_songs(self, songs: Union[set[str], list[str], list[Song]]) -> None:
        song_track_ids = set()

        for song in songs:
            if isinstance(song, Song):
                song_track_ids.add(song.track_id)
            else:
                song_track_ids.add(song)

        try:
            remove_songs_from_playlist(song_track_ids, self.spotify_id)
        except Exception as e:
            logger.error(f'Failed to remove songs from playlist {self.name}')
            logger.exception(e)
        else:
            logger.info(f'Succesfully removed songs from playlist {self.name}')
            self.songs.difference_update(song_track_ids)

    def remove_all_songs(self) -> None:
        logger.info(f'Removing all songs from playlist {self.name}')
        self.remove_songs(self.songs)
        