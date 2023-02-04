import bs4
import requests
from .package_logging import logger


def get_zlote_przeboje_day() -> list[tuple[str, str]]:
    """
     Pobierz informację o piosenkach granych w ciągu ostatniego dnia w Radiu Złote Przeboje
    """

    logger.info("Getting songs played yestarday in Zlote Przeboje radio")

    przeboje_html = requests.get("https://audycje.zloteprzeboje.tuba.pl/co-gralismy#TRNavSST")
    przeboje_html.raise_for_status()

    przeboje_soup = bs4.BeautifulSoup(przeboje_html.content, "html.parser")

    przeboje_songs_day = []

    przeboje_songs = przeboje_soup.select(f'.gra-ramowka-row')

    for song in przeboje_songs:
        artist = song.select('.gra-ramowka-row__primary-text')[0].get_text()
        title = song.select('.gra-ramowka__row__secondary-text')[0].get_text()

        if artist.find('&') != -1:
            artist = artist[:(artist.find('&')-1)]

        przeboje_songs_day.append((artist, title))

    return przeboje_songs_day
