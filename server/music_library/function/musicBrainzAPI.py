import requests
import json
import pprint

import acoustid
import logging
import musicbrainzngs
from django.conf import settings

data={}
print("[ ] lettura credenziali")
try:
    with open('credentials.json', 'r') as file:
        data = json.load(file)
    
    print(data)
except FileNotFoundError:
    print("File non trovato!")
except json.JSONDecodeError:
    print("Errore nel parsing del JSON!")

email = data["MUSIC_BRAINZ_API_EMAIL"]

#testare se legge il giusto file
from .error import *

logger = logging.getLogger(__name__)
email = settings.MUSIC_BRAINZ_API_EMAIL
>>>>>>> Stashed changes

headers = {
    f"User-Agent": "Music_library/1.0 ({email})"
}

def getMetadataByArtistID(artistID):
    try:
        return requests.get(f"https://musicbrainz.org/ws/2/artist/{artistID}?inc=url-rels&fmt=json").json()
    except Exception as error:
        return error

def getMetadataByrecordingID(recordingID):
    try:
        return requests.get(f"https://musicbrainz.org/ws/2/recording/{recordingID}?inc=artist-credits+annotation&fmt=json").json()
    except Exception as error:
        return error
    
def getMetadataByAlbumID(albumID):
    try:
        return requests.get(f"https://musicbrainz.org/ws/2/release/{albumID}?inc=artist-credits&fmt=json").json()
    except Exception as error:
        return error
    
<<<<<<< Updated upstream
=======
def getMetadataByTitleAndArtist(song_title, artist_name):
    try:

        result = musicbrainzngs.search_recordings(query=song_title, artist=artist_name, limit=1)
        recordings = result.get("recording-list", [])
        if recordings:
            recording = recordings[0]
            title = recording.get("title")
            # Le release vengono incluse in una chiave come "release-list"
            releases = recording.get("release-list", [])
            if releases:
                # Potresti avere più release, ad esempio versioni in diversi paesi o il lato B di un singolo.
                # Qui, prendiamo la prima come esempio.
                album = releases[0]
                album_id = album.get("id")
                album_title = album.get("title")
                print(f"Titolo: {title}\nAlbum: {album_title} (ID: {album_id})")
            else:
                print(f"Trovata registrazione '{title}', ma nessuna release associata.")
        else:
            print("Nessun risultato trovato")
        return album_id
    except Exception as error:
        return error

>>>>>>> Stashed changes
def getCoverAlbumByAlbumID(albumID):
    try:
        return requests.get(f"https://coverartarchive.org/release/{albumID}?fmt=json", timeout=10).json()
    except requests.exceptions.Timeout:
        raise requests.exceptions.Timeout
    except Exception as error:
        return error
    