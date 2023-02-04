import bs4
import requests
import concurrent.futures
from .package_logging import logger


def get_rmf_top() -> list[tuple[str, str]]:
    """
     Pobierz stronę rmf z notowaniem i wyszukaj na niej odpowiednie elementy, zwróc listę zwierającą tuple z artystą i tytułem
    """

    logger.info("Getting songs from Rmf top list")

    rmf_html = requests.get("https://www.rmf.fm/au/?a=poplista")
    rmf_html.raise_for_status()

    rmf_soup = bs4.BeautifulSoup(rmf_html.content, "html.parser")

    rmf_songs_top = []

    rmf_songs = rmf_soup.select('.poplista-artist-title')

    for song in rmf_songs:
        if len(song.select('a')) < 1:
            continue
        artist = song.select('a')[0].get_text()
        title = song.get_text().replace(artist, '')

        if artist.find('feat.') != -1:
            artist = artist[:(artist.find('feat.')-1)]

        if artist.find('x') != -1 and artist[artist.find('x') - 1] == ' ':
            artist = artist[:(artist.find('x') - 1)]

        rmf_songs_top.append((artist, title))

    return rmf_songs_top


def _get_rmf_item_details(item_id: str) -> dict:
    """
     Pobranie informacji z api rmf na temat piosenek o danym item_id
    """

    query = f'https://live.rmf.fm/items.html?ids={item_id}'

    response = requests.get(query)

    return response.json()


def get_rmf_day() -> list[tuple[str, str]]:
    """
     Pobierz informację o piosenkach granych w ciągu ostatniego dnia w RmfFm
    """

    logger.info("Getting songs played yestarday in RmfFm radio")

    response = requests.get('https://live.rmf.fm/items-list.html')
    response.raise_for_status()

    ids = []

    for item in response.json():
        if item['category'] == 'song':
            ids.append(item['ID'])

    rmf_songs_day = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(_get_rmf_item_details, ids)

    for result in results:
        item_id = list(result.keys())[0]
        if len(result[item_id]['title'].split(' - ')) >= 3:
            artist = result[item_id]['title'].split(' - ')[0]
            title = result[item_id]['title'].split(' - ')[-1]
        else:
            artist, title = result[item_id]['title'].split(' - ')

        if artist.find('/') != -1:
            artist = artist[:(artist.find('/')-1)]

        rmf_songs_day.append((artist, title))

    return rmf_songs_day
