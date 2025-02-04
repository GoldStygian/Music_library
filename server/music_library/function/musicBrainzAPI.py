import requests
import json
import pprint

import acoustid
import musicbrainzngs

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
    
def getCoverAlbumByAlbumID(albumID):
    try:
        return requests.get(f"https://coverartarchive.org/release/{albumID}?fmt=json", timeout=10).json()
    except requests.exceptions.Timeout:
        raise requests.exceptions.Timeout
    except Exception as error:
        return error