from itertools import islice
import concurrent.futures


def make_chunks(data: list, size: int) -> list:
    """
     Divide list into chunks of a given size
    """
    it = iter(data)
    for i in range(0, len(data), size):
        yield [k for k in islice(it, size)]


def _create_song_obj(tuplet: tuple[str, str]):
    from .song import Song

    artist, title = tuplet
    return Song(artist, title)


def create_song_objects_from_list(tuple_list: list[tuple[str, str]]) -> list[any]:
    """
     Create and return list of song objects created from list of tuples containing artist and title
    """
    objects = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(_create_song_obj, tuple_list)

    for result in results:
        objects.append(result)

    return objects
