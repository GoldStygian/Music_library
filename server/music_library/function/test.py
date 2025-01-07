import acoustid
import musicbrainzngs

import pprint
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
import json

# Inserisci qui la tua chiave API di MusicBrainz
ACOUSTID_API_KEY = 'z6uxCKyMbZ'

# Impostazioni per MusicBrainz
musicbrainzngs.set_useragent("Music Library", "1.0")

def get_acoustic_id(file_path):
    # Estrai l'ID acustico e cerca informazioni tramite AcoustID
    try:
        duration, fingerprint = acoustid.fingerprint_file(file_path)
        # Richiesta al servizio AcoustID
        results = acoustid.lookup(ACOUSTID_API_KEY, fingerprint, duration)
        for score, recording_id, title, artist in parse_acoustid_results(results):
            return recording_id  # Restituisce il recording ID da usare con MusicBrainz
    except acoustid.AcoustidError as e:
        print(f"Errore nella generazione dell'AcousticID: {e}")
        return None

def parse_acoustid_results(results):
    # Processa i risultati restituiti da AcoustID
    try:
        for result in results["results"]:
            score = result["score"]
            recording = result["recordings"][0]
            recording_id = recording["id"]
            title = recording.get("title", "Unknown")
            # artist = recording["artists"][0].get("name", "Unknown")
            artist = "test"
            yield score, recording_id, title, artist
    except KeyError:
        print("Errore nel parsing dei risultati AcoustID")

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

def identify_track(file_path):
    recording_id = get_acoustic_id(file_path)
    if recording_id:
        result = lookup_musicbrainz(recording_id)
        if result:
            # Convertiamo l'oggetto Python in una stringa JSON
            return json.dumps(result)

# Esegui l'identificazione del file audio
file_path = r"C:\Users\prora\Desktop\Il mio video.mp3"#r"C:\Users\prora\Desktop\Music_library\server\media\Don Omar\Don Omar - Virtual Diva.mp3"
json_metadata = identify_track(file_path)

def update_metadata(file_path, metadata):

    # Mappatura dei metadati richiesti
    def map_metadata(result_output):
        recording = result_output.get("recording", {})
        artist_credit = recording.get("artist-credit", [{}])[0].get("artist", {})
        release_list = recording.get("release-list", [{}])[0]
        
        # Metadati richiesti
        metadata = {
            "album": release_list.get("title", "Unknown Album"),
            "bpm": recording.get("bpm", ""),  # Aggiungi un valore di fallback vuoto
            "length": recording.get("length", ""),  # Aggiungi un valore di fallback vuoto
            "media": "Digital Media",  # Valore predefinito
            "title": recording.get("title", "Unknown Title"),
            "artist": artist_credit.get("name", "Unknown Artist"),
            "albumartist": artist_credit.get("name", "Unknown Album Artist"),
            "discnumber": "1/1",  # Valore predefinito
            "organization": "Unknown Organization",  # Valore predefinito
            "tracknumber": "1/1",  # Valore predefinito
            "artistsort": artist_credit.get("sort-name", "Unknown Sort Name"),
            "isrc": recording.get("isrc", ""),  # Aggiungi un valore di fallback vuoto
            "genre": recording.get("genre", "Unknown Genre"),  # Aggiungi un valore di fallback
            "date": release_list.get("date", ""),
            "originaldate": release_list.get("date", ""),
            "musicbrainz_trackid": recording.get("id", ""),
            "musicbrainz_artistid": artist_credit.get("id", ""),
            "musicbrainz_albumid": release_list.get("id", ""),
            "musicbrainz_albumartistid": artist_credit.get("id", ""),
            "musicbrainz_albumstatus": "official",  # Valore predefinito
            "musicbrainz_albumtype": "album",  # Valore predefinito
            "barcode": release_list.get("barcode", ""),
            "musicbrainz_releasetrackid": recording.get("release-trackid", ""),  # Aggiungi un valore di fallback
            "musicbrainz_releasegroupid": recording.get("release-groupid", ""),  # Aggiungi un valore di fallback
            "acoustid_id": recording.get("acoustid_id", ""),  # Aggiungi un valore di fallback
            "id": recording.get("id", "")
        }
        
        return metadata

    # Controlla l'estensione del file
    if file_path.endswith(".mp3"):
        audio = EasyID3(file_path)
    elif file_path.endswith(".flac"):
        audio = FLAC(file_path)
    else:
        raise ValueError("Formato non supportato! Usa solo MP3 o FLAC.")
    
    # Aggiungi i metadati principali
    mapped_metadata = map_metadata(metadata)

    audio["title"] = mapped_metadata.get("title", "Unknown")
    audio["artist"] = mapped_metadata.get("artist", "Unknown")
    audio["albumartist"] = mapped_metadata.get("albumartist", "Unknown")
    audio["discnumber"] = mapped_metadata.get("discnumber", "1/1")
    audio["organization"] = mapped_metadata.get("organization", "Unknown Organization")
    audio["tracknumber"] = mapped_metadata.get("tracknumber", "1/1")
    audio["artistsort"] = mapped_metadata.get("artistsort", "Unknown Sort Name")
    audio["isrc"] = mapped_metadata.get("isrc", "")
    audio["genre"] = mapped_metadata.get("genre", "Unknown Genre")
    audio["date"] = mapped_metadata.get("date", "Unknown")
    audio["originaldate"] = mapped_metadata.get("originaldate", "Unknown")
    audio["musicbrainz_trackid"] = mapped_metadata.get("musicbrainz_trackid", "")
    audio["musicbrainz_artistid"] = mapped_metadata.get("musicbrainz_artistid", "")
    audio["musicbrainz_albumid"] = mapped_metadata.get("musicbrainz_albumid", "")
    audio["musicbrainz_albumartistid"] = mapped_metadata.get("musicbrainz_albumartistid", "")
    audio["musicbrainz_albumstatus"] = mapped_metadata.get("musicbrainz_albumstatus", "official")
    audio["musicbrainz_albumtype"] = mapped_metadata.get("musicbrainz_albumtype", "album")
    audio["barcode"] = mapped_metadata.get("barcode", "")
    audio["musicbrainz_releasetrackid"] = mapped_metadata.get("musicbrainz_releasetrackid", "")
    audio["musicbrainz_releasegroupid"] = mapped_metadata.get("musicbrainz_releasegroupid", "")
    audio["acoustid_id"] = mapped_metadata.get("acoustid_id", "")
    
    # Opzionale: Aggiungi dettagli dell'album
    release_list = mapped_metadata.get("release-list", [])
    if release_list:
        # Prendi il primo album come principale
        first_release = release_list[0]
        audio["album"] = first_release.get("title", "Unknown")
        audio["date"] = first_release.get("date", "Unknown")
    
    # Salva i metadati
    audio.save()

# Aggiorna i metadati del file audio
try:
    update_metadata(file_path, json.loads(json_metadata))
    print(f"Metadati aggiornati con successo per il file: {file_path}")
except Exception as e:
    print(f"Errore durante l'aggiornamento dei metadati: {e}")