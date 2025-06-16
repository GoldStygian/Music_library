import acoustid
import musicbrainzngs
import pprint
from django.conf import settings
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
import logging

logger = logging.getLogger(__name__)
ACOUSTID_API_KEY = settings.ACOUSTID_API_KEY
musicbrainzngs.set_useragent("Music Library", "1.0")

def get_acoustic_id(file_path):

    try:
        duration, fingerprint = acoustid.fingerprint_file(file_path)

        logging.info("Fingerprint: ", fingerprint)
        return fingerprint
    except acoustid.AcoustidError as e:
        print(f"Errore nella generazione dell'AcousticID: {e}")
        return None


def lookup_musicbrainz(recording_id):
    # Cerca i dettagli del brano su MusicBrainz utilizzando il recording ID
    try:
        result = musicbrainzngs.get_recording_by_id(recording_id, includes=["artists", "releases"])
        # Nome del file in cui vuoi scrivere il risultato
        file_path = r"./result_output.txt"

        # Scrivi il risultato su un file
        with open(file_path, "w", encoding="utf-8") as file:
            pprint.pprint(result, stream=file)

        recording = result["recording"]
        title = recording["title"]
        artist = "test"
        # artist = recording["artist-credit"][0]["name"]
        album = recording.get("release-list", [{}])[0].get("title", "Unknown")
        print(f"Track found:\ntitle: {title}\nartist: {artist}\nAlbum: {album}")

        if result:
            return result

    except musicbrainzngs.WebServiceError as e:
        print(f"Errore nella ricerca su MusicBrainz: {e}")

    return None


def get_song_data(file_path):
    try:
        duration, fingerprint = acoustid.fingerprint_file(file_path)

        logging.info("Fingerprint generato con successo")

        results = acoustid.lookup(ACOUSTID_API_KEY, fingerprint, duration)

        for result in results['results']:
            print("AAAAAAAAAAAAAA", result)
            if 'recordings' in result:
                recording = result['recordings'][0]
                title = recording.get('title')
                artist = recording['artists'][0]['name'] if 'artists' in recording else "Sconosciuto"
                recording_id = recording['id']

                # Cerca release associata all'enregistrement
                album_id = None
                album_title = None

                if 'releases' in recording and recording['releases']:
                    release = recording['releases'][0]
                    album_id = release.get('id')
                    album_title = release.get('title')

                return {
                    'title': title,
                    'artist': artist,
                    'recording_id': recording_id,
                    'album_id': album_id,
                    'album_title': album_title
                }

        return None  # Nessun risultato utile

    except acoustid.AcoustidError as e:
        print(f"Errore nella generazione dell'AcousticID: {e}")
        return None
