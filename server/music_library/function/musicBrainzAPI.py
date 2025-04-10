import requests
import json
import pprint
import logging

import acoustid
import musicbrainzngs

from .error import *

logger = logging.getLogger(__name__)

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

# Testare se legge il giusto file

header = {
    f"User-Agent": "Music_library/1.5 ({email})"
}

def getMetadataByArtistID(artistID):
    try:
        response = requests.get(f"https://musicbrainz.org/ws/2/artist/{artistID}?inc=url-rels&fmt=json", headers=header)
        logging.info(f"Request at MusciBrainz API: {response.url}")
        response = response.json()
        logging.info(f"Response: {response}")

        try: 
            if response["error"]: raise MusciBrainzError.MusicBrainzLimitRequestExceeding
        except KeyError:pass

        return response
    except Exception as error:
        return error

def getMetadataByrecordingID(recordingID):
    try:
        response = requests.get(f"https://musicbrainz.org/ws/2/recording/{recordingID}?inc=artist-credits+annotation&fmt=json", headers=header)
        logging.info(f"Request at MusciBrainz API: {response.url}")
        response = response.json()
        logging.info(f"Response: {response}")
        return response
    except Exception as error:
        return error
    
def getMetadataByAlbumID(albumID):
    try:
        response = requests.get(f"https://musicbrainz.org/ws/2/release/{albumID}?inc=artist-credits&fmt=json", headers=header)
        logging.info(f"Request at MusciBrainz API: {response.url}")
        response = response.json()
        logging.info(f"Response: {response}")
        return response
    except Exception as error:
        return error

def getCoverAlbumByAlbumID(albumID):
    try:
        response = requests.get(f"https://coverartarchive.org/release/{albumID}?fmt=json", headers=header, timeout=10)
        logging.info(f"Request at MusciBrainz API: {response.url}")
        response = response.json()
        logging.info(f"Response: {response}")
        return response
    except requests.exceptions.Timeout:
        raise requests.exceptions.Timeout
    except Exception as error:
        return error