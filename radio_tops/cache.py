import redis
import redis.exceptions
from typing import Union, TYPE_CHECKING
from .package_logging import logger
from .config import settings

if TYPE_CHECKING:
    from .song import Song


def save_to_cache(song: "Song", track_id: str) -> None:
    """
    saving data to cache
    """
    logger.debug(f'Saving {song.artist} {song.title} to cache with value {track_id}')
    try:
        r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
        r.set(f'{song.artist} {song.title}', track_id)
    except ConnectionRefusedError as e:
        logger.error('Redis server refused connection')
        logger.exception(e)
    except redis.exceptions.ConnectionError as e:
        logger.error('Connection to redis server failed')
        logger.exception(e)


def read_from_cache(song: "Song") -> Union[None, str]:
    """
    reading data from cache
    """

    result = None

    try:
        r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
        result = r.get(f'{song.artist} {song.title}')
    except ConnectionRefusedError as e:
        logger.error('Redis server refused connection')
        logger.exception(e)
    except redis.exceptions.ConnectionError as e:
        logger.error('Connection to redis server failed')
        logger.exception(e)

    if result is not None:
        logger.debug(f'Got response from cache for {song.artist} {song.title} with value {result}')
        return result.decode('utf-8')

    logger.debug(f'Got response from cache for {song.artist} {song.title}. Key not found.')
    return result
