import requests
import json
from typing import Union, Set, Any
from .helpers import make_chunks
from .package_logging import logger
from .config import settings

TOKEN = None

SPOTIFY_PLAYER_BASE_URL = 'https://open.spotify.com'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'


def get_token() -> str:
    """
    obtain token from api
    """
    global TOKEN

    if TOKEN is not None:
        return TOKEN

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"

    session = requests.Session()
    cookies = {'sp_dc': settings.sp_dc, 'sp_key': settings.sp_key}
    headers = {'user-agent': user_agent}

    logger.info('Trying to obtain spotify token from api')
    response = session.get(f'{SPOTIFY_PLAYER_BASE_URL}/get_access_token?reason=transport&productType=web_player',
                               headers=headers, cookies=cookies)

    response.raise_for_status()

    data = response.content.decode("utf-8")
    config = json.loads(data)

    TOKEN = config['accessToken']
    return TOKEN


def get_track_id(artist: str, title: str) -> Union[None, str]:
    """
    obtaining track_id based on artist and title from spotify api
    """

    token = get_token()

    query = f'{SPOTIFY_API_BASE_URL}/search?query=track%3A{title}+artist%3A{artist}&type=track&offset=0&limit=20'
    logger.debug(f'Quering api for track_id for song {artist} - {title}')
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )
    response_json = response.json()
    # logger.debug(f'Api response: {response_json}')
    songs = response_json["tracks"]["items"]

    # Jeżeli znaleziono jakieś piosenki zwróc uri pierwszej z nich
    if len(songs) != 0:
        # only use the first song
        uri = songs[0]["uri"]
        return uri

    # Jeśli nie znaleziono żadnej piosenki zwróc None
    logger.warning(f'{artist} - {title} not found in spotify api')
    return None


def create_playlist(name: str, desc: str, public: bool) -> str:
    """
     creating a playlist
    """
    token = get_token()

    request_body = json.dumps({
        "name": name,
        "description": desc,
        "public": public
    })

    logger.debug(f'Trying to create plalist {name}')
    query = f'{SPOTIFY_API_BASE_URL}/users/{settings.spotify_user_id}/playlists'
    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )

    response.raise_for_status()

    response_json = response.json()

    logger.info(f'Playlist {name} created with id {response_json["id"]}')

    response_json = response.json()
    logger.debug(f'Api response {response_json}')

    # playlist id
    return response_json["id"]


def add_songs_to_playlist(songs: Union[set[str], list[str]], playlistid: str) -> None:
    """
     Split given array of songs into chunks
    """
    if len(songs) < 100:
        _add_songs_to_playlist_call(songs, playlistid)
        return

    for chunk in make_chunks(songs, 100):
        logger.debug('Adding items to playlist in chunks, becouse too many elements')
        _add_songs_to_playlist_call(chunk, playlistid)


def _add_songs_to_playlist_call(songs: Union[set[str], list[str]], playlistid: str) -> dict:
    """
     Add given songs (in form of a list of track_ids) to a given playlist
    """

    token = get_token()

    request_body = json.dumps(list(songs))

    query = f'{SPOTIFY_API_BASE_URL}/playlists/{playlistid}/tracks'

    logger.debug(f'Adding songs to playlist. Songs: {request_body}')
    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )
    logger.debug(f'Api response: {response.json()}')

    return response.json()


def remove_songs_from_playlist(songs: Union[set[str], list[str]], playlistid: str) -> None:
    """
     Split given array of songs into chunks
    """
    if len(songs) < 100:
        _remove_songs_from_playlist_call(songs, playlistid)
        return

    for chunk in make_chunks(songs, 100):
        logger.debug('Removing items from playlist in chunks, becouse too many elements')
        _remove_songs_from_playlist_call(chunk, playlistid)


def _remove_songs_from_playlist_call(songs: Union[set[str], list[str]], playlistid: str) -> dict:
    """
     Delete a playlist items (itemlist is a object returned by getPlaylistItems)
    """

    token = get_token()

    # Converting list of track_ids to object accepted by API
    request_body = {'tracks': []}
    for song in songs:
        if song is not None:
            request_body['tracks'].append({'uri': song})

    body_data_json = json.dumps(request_body)

    logger.debug(f'Removing songs from playlist. Songs: {request_body}')

    query = f'{SPOTIFY_API_BASE_URL}/playlists/{playlistid}/tracks'

    response = requests.delete(
        query,
        data=body_data_json,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )

    logger.debug(f'Api response: {response.json()}')

    return response.json()


def get_playlist_items(playlistid: str) -> set[str]:
    """
     Read items from a given playlist
    """
    songs = set()
    token = get_token()

    logger.debug(f'Quering api for playlist {playlistid} items')

    query = f'{SPOTIFY_API_BASE_URL}/playlists/{playlistid}/tracks?fields=items(track(name%2C%20uri)),next'
    response = _get_playlist_items_call(query, token)

    for item in response["items"]:
        songs.add(item["track"]["uri"])

    while True:
        if response["next"] is None:
            break

        response = _get_playlist_items_call(response["next"], token)
        for item in response["items"]:
            songs.add(item["track"]["uri"])

    logger.debug(f'Songs in playlist {playlistid}: {songs}')
    return songs


def _get_playlist_items_call(url: str, token: str) -> set[str]:
    """
     Read items from a given url
    """
    logger.debug(f'Quering api for playlist items with url {url}')
    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )
    response.raise_for_status()
    return response.json()


def remove_playlist(playlistid: str) -> dict:
    """
     Remove playlist
    """

    token = get_token()

    logger.debug(f'Removing playlist with id {playlistid}')
    query = f'{SPOTIFY_API_BASE_URL}/playlists/{playlistid}/followers'
    response = requests.delete(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )

    response.raise_for_status()

    logger.info(f'Removed playlist with id {playlistid}')
    logger.debug(f'Api response {response.json()}')

    return response.json()
