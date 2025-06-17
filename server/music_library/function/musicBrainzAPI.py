import requests
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)
email = settings.MUSIC_BRAINZ_API_EMAIL

HEADERS = {
    "User-Agent": f"Music_library/1.0 ({email})"
}

def _fetch_json(url):
    resp = requests.get(url, headers=HEADERS, timeout=10)
    data = resp.json()
    if isinstance(data, dict) and data.get('error'):
        # Solleva un'eccezione con il messaggio restituito da MusicBrainz
        raise Exception(f"MusicBrainz API error: {data['error']}")
    return data

def getMetadataByArtistID(artistID):
    """
    Ottiene i metadati dell'artista. Se la risposta contiene 'error',
    viene sollevata un'eccezione con il messaggio di errore.
    """
    try:
        url = f"https://musicbrainz.org/ws/2/artist/{artistID}?inc=url-rels&fmt=json"
        return _fetch_json(url)
    except Exception as error:
        logger.error(f"Errore in getMetadataByArtistID({artistID}): {error}")
        raise

def getMetadataByrecordingID(recordingID):
    """
    Ottiene i metadati della registrazione. Solleva eccezione se 'error' è presente.
    """
    try:
        url = f"https://musicbrainz.org/ws/2/recording/{recordingID}?inc=artist-credits+annotation&fmt=json"
        return _fetch_json(url)
    except Exception as error:
        logger.error(f"Errore in getMetadataByrecordingID({recordingID}): {error}")
        raise

def getMetadataByAlbumID(albumID):
    """
    Ottiene i metadati della release (album). Solleva eccezione se 'error' è presente.
    """
    try:
        url = f"https://musicbrainz.org/ws/2/release/{albumID}?inc=artist-credits&fmt=json"
        return _fetch_json(url)
    except Exception as error:
        logger.error(f"Errore in getMetadataByAlbumID({albumID}): {error}")
        raise

def getCoverAlbumByAlbumID(albumID):
    """
    Ottiene la cover dal CoverArtArchive. Timeout diverso dagli altri errori.
    """
    try:
        url = f"https://coverartarchive.org/release/{albumID}?fmt=json"
        data = requests.get(url, timeout=10).json()
        if isinstance(data, dict) and data.get('error'):
            raise Exception(f"CoverArtArchive error: {data['error']}")
        return data
    except requests.exceptions.Timeout:
        logger.error(f"Timeout fetching cover for album {albumID}")
        raise
    except Exception as error:
        logger.error(f"Errore in getCoverAlbumByAlbumID({albumID}): {error}")
        raise
