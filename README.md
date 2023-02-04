# Opis

Aplikacja pobierająca topki stacji radiowych oraz wszystkie grane w danym dniu i tworząca na tej podstawie playlisty na spotify

## Docker

Budowanie
```bash
docker build --tag radio_tops_spotify .
```

Configuracja
W katalogu z plikiem docker-compose należy utworzyć `config.env` z konfiguracją, dostępne opcje:
- `RADIO_TOPS_SPOTIFY_USER_ID` - **WYMAGANE**
- `RADIO_TOPS_SP_DC` - **WYMAGANE**
- `RADIO_TOPS_SP_KEY` - **WYMAGANE**
- `RADIO_TOPS_ENABLE_CACHE` - czy włączyć cachowanie id piosenek (w opraciu o REDIS) (domyślnie: False)
- `RADIO_TOPS_REDIS_HOST` - adres serwera REDIS (domyślnie: localhost)
- `RADIO_TOPS_REDIS_PORT` - port serwera REDIS (domyślnie: 6379)
- `RADIO_TOPS_REDIS_DB` - numer db w redis (domyślnie: 0)
- `RADIO_TOPS_LOG_LEVEL_DEBUG` - czy włączyć DEBUG (domyślnie: False)
- `RADIO_TOPS_PLAYLIST_IDS_FILE` - ścieżka do pliku z id playlist (domyślnie: playlist_ids.json)
- `RADIO_TOPS_PLAYLISTS_PUBLIC` - czy playlisty mają być publiczne (domyślnie: False)


Uruchamianie
```bash
docker-compose -f <ścieżka do pliku doker_compose> up
```

## Pozyskiwanie sp_dc i sp_key

1. Zalogować się na stronie open.spotify.com
2. Wejść w narzędzia deweloperskie przeglądarki
3. Przejść do sekcji z plikami cookies

# Wpis cron:
```bash
30 23 * * * root /bin/docker-compose -f /opt/docker/radio_tops_spotify/docker-compose.yml up  2>&1 1> /opt/docker/radio_tops_spotify/log/`date +"\%Y-\%m-\%d_\%H-\%M"`.log
```

## Playlisty wygenerowane przez skrypt

- [Złote Przeboje - jeden dzień](https://open.spotify.com/playlist/74oo50UonEnHO4Vl9EEbnY?si=fe4446a0c8bf4e38)
- [RmfFm - jeden dzień](https://open.spotify.com/playlist/0EQIMYsEBm0jJnqRw9qHwf?si=8283c98a6deb471e)
- [Eska - jeden dzień](https://open.spotify.com/playlist/6WLPrKiM6VaS73csIpUk0n?si=281bde54a38d4bd4)
- [RMF PopLista](https://open.spotify.com/playlist/1hFhmK4sbMqItMDrqHUkMn?si=54d8849904754dc0)
- [Gorąca 20-estka](https://open.spotify.com/playlist/4KA7wKHZRfF2un3sH3cpP8?si=c53faab597b944ec)