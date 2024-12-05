import requests
from django.conf import settings

def get_artist_image_from_lastfm(mb_artist_id, last_fm_api_key):

    # URL dell'API di Last.fm per ottenere dettagli dell'artista
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&mbid={mb_artist_id}&api_key={last_fm_api_key}&format=json"
    response = requests.get(url)
    data = response.json()
    
    # Controlla per immagini diverse
    image_url = None
    for image in data.get("artist", {}).get("image", []):
        if image["size"] == "extralarge" and "default" not in image["#text"]:
            image_url = image["#text"]
            break
    return image_url