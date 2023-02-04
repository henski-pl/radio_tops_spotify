from .spotify import get_track_id
from .cache import read_from_cache, save_to_cache
from .config import settings

STATS = {
    'songs_found_api': 0,
    'songs_found_cache': 0,
    'songs_unfound': 0,
}


class Song:

    def __init__(self, artist: str, title: str):
        self.artist = artist
        self.title = title
        self.track_id = self.__track_id()

    def __track_id(self) -> str:
        if settings.enable_cache:
            cache = read_from_cache(self)
        else:
            cache = None

        # If response from redis is None, or cache is disabled, ask API
        if cache is None:
            track_id = get_track_id(self.artist, self.title)
            # If response from API is diffrent than None save that response to cache
            if track_id is not None:
                STATS['songs_found_api'] += 1
                if settings.enable_cache:
                    save_to_cache(self, track_id)
            else:
                STATS['songs_unfound'] += 1
        else:
            STATS['songs_found_cache'] += 1
            track_id = cache

        self.track_id = track_id
        return track_id
