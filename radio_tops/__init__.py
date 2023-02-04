import time
from typing import Callable
from .playlist import Playlist
from .package_logging import logger
from .helpers import create_song_objects_from_list
from .collector_rmf import get_rmf_day, get_rmf_top
from .collector_eska import get_eska_day, get_eska_top
from .collector_zlote_przeboje import get_zlote_przeboje_day
from .song import STATS
from .config import settings


def create_ready_playlist(name: str, desc: str, public: bool, collector_function: Callable) -> Playlist:
    logger.info(f'Creating ready playlist {name}')
    ready_playlist = Playlist(name, desc, public)

    songs_list = collector_function()
    songs = create_song_objects_from_list(songs_list)

    logger.info(f'Adding songs to playlist {name}')
    ready_playlist.remove_all_songs()
    ready_playlist.add_songs(songs)

    return ready_playlist


def create_playlists() -> None:
    logger.info('#### START ####')
    time_start = time.perf_counter()

    playlist_rmf_day = create_ready_playlist('Rmf - jeden dzień', 'Playlista z piosenkami granymi w radiu rmf wczoraj', settings.playlists_public, get_rmf_day)
    playlist_rmf_top = create_ready_playlist('Rmf PopLista', 'Playlista z aktualnym notawaniem POPlisty', settings.playlists_public, get_rmf_top)

    playlist_eska_day = create_ready_playlist('Eska - jeden dzień', 'Playlista z piosenkami granymi w radiu eska wczoraj', settings.playlists_public, get_eska_day)
    playlist_eska_top = create_ready_playlist('Gorąca 20-estka', 'Playlista z aktualną gorącą 20-estką', settings.playlists_public, get_eska_top)

    playlist_przeboje_day = create_ready_playlist('Złote Przeboje - jeden dzień', 'Playlista z piosenkami granymi w radiu Złote Przeboje wczoraj', settings.playlists_public, get_zlote_przeboje_day)

    time_stop = time.perf_counter()
    logger.info('#### DONE ####')
    logger.info(f'Songs found in api: {STATS["songs_found_api"]}')
    logger.info(f'Songs found in cache: {STATS["songs_found_cache"]}')
    logger.info(f'Songs unfound: {STATS["songs_unfound"]}')
    logger.info(f'Total execution time: {round(time_stop - time_start, 2)} second(s)')

