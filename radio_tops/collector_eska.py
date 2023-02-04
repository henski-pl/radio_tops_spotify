from typing import List, Tuple, Any

import bs4
from datetime import date, timedelta
import requests
import concurrent.futures
from .package_logging import logger


def get_eska_top() -> list[tuple[str, str]]:
    """
     Pobierz stronę eski z notowaniem i wyszukaj na niej odpowiednie elementy, zwróc listę zwierający artystów i tytuły
    """

    logger.info("Getting songs from Eska top list")
    eska_html = requests.get("https://www.eska.pl/goraca20/")

    eska_html.raise_for_status()

    eska_soup = bs4.BeautifulSoup(eska_html.content, "html.parser")

    eska_songs = eska_soup.select('.single-hit__info')

    eska_songs_top = []

    for song in eska_songs:
        title = song.select('.single-hit__title')[0].get_text()
        artist = song.select('.single-hit__author')[0].get_text()
        if title != 'Radio ESKA':
            eska_songs_top.append((artist, title))

    return eska_songs_top


def _get_eska_hour_songs(hour: str) -> dict:
    """
     Pobranie informacji z api eski na temat piosenek granych o danej godzinie
    """

    yesterday = date.today() - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    query = f'https://www.eska.pl/jsonapi/whatWasPlayed?id=999&date={yesterday}&teaser=false&hour={hour}'

    response = requests.get(query)

    return response.json()


def get_eska_day() -> list[tuple[str, str]]:
    """
     Pobierz informację o piosenkach granych w ciągu ostatniego dnia w Eska
    """

    logger.info("Getting songs played yestarday in Eska radio")

    hours = range(24)

    eska_songs_day = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(_get_eska_hour_songs, hours)

    for result in results:
        for song in result:
            title = song['name']
            artist = song['artists'][0]['name']

            eska_songs_day.append((artist, title))

    return eska_songs_day
