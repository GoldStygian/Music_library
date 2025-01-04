import requests
import json

# fare la calsse con il metodo di inizzializzazione

import acoustid
import musicbrainzngs

# Inserisci qui la tua chiave API di MusicBrainz
API_KEY = 'your_musicbrainz_api_key'

# Impostazioni per MusicBrainz
musicbrainzngs.set_useragent("AcousticIDApp", "1.0", API_KEY)

def get_acoustic_id(file_path):
    # Estrai l'ID acustico dal file audio
    try:
        # Genera l'ID acustico
        duration, fingerprint = acoustid.fingerprint_file(file_path)
        return fingerprint
    except acoustid.AcoustidError as e:
        print(f"Errore nella generazione dell'AcousticID: {e}")
        return None

def lookup_musicbrainz(acoustic_id):
    # Cerca il brano su MusicBrainz utilizzando l'AcousticID
    try:
        result = musicbrainzngs.lookup_recording(acoustic_id)
        if result:
            recording = result['recording']
            title = recording['title']
            artist = recording['artist-credit'][0]['name']
            album = recording.get('release-list', [{}])[0].get('title', 'Unknown')
            print(f"Track found: {title} by {artist}, Album: {album}")
    except musicbrainzngs.WebServiceError as e:
        print(f"Errore nella ricerca su MusicBrainz: {e}")

def identify_track(file_path):
    acoustic_id = get_acoustic_id(file_path)
    if acoustic_id:
        lookup_musicbrainz(acoustic_id)

# Esegui l'identificazione del file audio
file_path = "path_to_your_audio_file.mp3"
identify_track(file_path)


# -----

headers = {
    "User-Agent": "Music_library/1.0 (raf.rai.python@outlook.it)"
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
    
#data = getMetadataByArtistID
#print(json.dumps(data, indent=4))

# artista OK
# https://musicbrainz.org/ws/2/artist/99efca32-eea1-45fb-92cb-8798976a9769?fmt=json
# {
#     "end-area": null,
#     "life-span": {
#         "begin": "1986-10-16",
#         "end": null,
#         "ended": false
#     },
#     "sort-name": "Inna",
#     "type": "Person",
#     "area": {
#         "id": "61ed84b8-5a10-30a7-8376-ccd51801d6d1",
#         "disambiguation": "",
#         "iso-3166-1-codes": [
#             "RO"
#         ],
#         "name": "Romania",
#         "type": null,
#         "type-id": null,
#         "sort-name": "Romania"
#     },
#     "name": "Inna",
#     "gender": "Female",
#     "disambiguation": "Romanian dance singer",
#     "isnis": [
#         "0000000114563419"
#     ],
#     "id": "99efca32-eea1-45fb-92cb-8798976a9769",
#     "begin-area": {
#         "disambiguation": "",
#         "id": "7ac5975b-f555-448e-9fc7-104b165795fc",
#         "iso-3166-2-codes": [
#             "RO-CT"
#         ],
#         "sort-name": "Constan\u021ba",
#         "type-id": null,
#         "type": null,
#         "name": "Constan\u021ba"
#     },
#     "country": "RO",
#     "gender-id": "93452b5a-a947-30c8-934f-6a4056b151c2",
#     "type-id": "b6e035f4-3ce9-331c-97df-83397230b0df",
#     "ipis": [
#         "00683847888"
#     ]
# }

# cover album
# "https://coverartarchive.org/release/69307f05-6182-4d73-bfad-0e11346b526f?fmt=json"

#recording
# https://musicbrainz.org/ws/2/recording/0810268f-2e52-4f89-86be-42762ea3f6d4?inc=artist-credits+annotation&fmt=json
# {
#   "first-release-date": "2008-04-08",
#   "id": "0810268f-2e52-4f89-86be-42762ea3f6d4",
#   "video": false,
#   "disambiguation": "",
#   "length": 241933,
#   "annotation": null,
#   "title": "Just Dance",
#   "artist-credit": [
#     {
#       "joinphrase": " featuring ",
#       "name": "Lady Gaga",
#       "artist": {
#         "sort-name": "Lady Gaga",
#         "type-id": "b6e035f4-3ce9-331c-97df-83397230b0df",
#         "id": "650e7db6-b795-4eb5-a702-5ea2fc46c848",
#         "type": "Person",
#         "disambiguation": "",
#         "name": "Lady Gaga"
#       }
#     },
#     {
#       "artist": {
#         "sort-name": "O’Donis, Colby",
#         "type-id": "b6e035f4-3ce9-331c-97df-83397230b0df",
#         "id": "d71c2b20-616a-4bb8-a848-e6edac412c3b",
#         "type": "Person",
#         "disambiguation": "",
#         "name": "Colby O’Donis"
#       },
#       "name": "Colby O’Donis",
#       "joinphrase": ""
#     }
#   ]
# }