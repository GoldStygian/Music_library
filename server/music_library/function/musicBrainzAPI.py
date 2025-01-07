import requests
import json


import acoustid
import musicbrainzngs
import pprint
# fare la calsse con il metodo di inizzializzazione

# ACOUSTID_API_KEY = 'z6uxCKyMbZ'

# # Impostazioni per MusicBrainz
# musicbrainzngs.set_useragent("Music Library", "1.0")

# def get_acoustic_id(file_path):
#     # Estrai l'ID acustico e cerca informazioni tramite AcoustID
#     try:
#         duration, fingerprint = acoustid.fingerprint_file(file_path)
#         # Richiesta al servizio AcoustID
#         results = acoustid.lookup(ACOUSTID_API_KEY, fingerprint, duration)
#         for score, recording_id, title, artist in parse_acoustid_results(results):
#             return recording_id  # Restituisce il recording ID da usare con MusicBrainz
#     except acoustid.AcoustidError as e:
#         print(f"Errore nella generazione dell'AcousticID: {e}")
#         return None

# def parse_acoustid_results(results):
#     # Processa i risultati restituiti da AcoustID
#     try:
#         for result in results["results"]:
#             score = result["score"]
#             recording = result["recordings"][0]
#             recording_id = recording["id"]
#             title = recording.get("title", "Unknown")
#             # artist = recording["artists"][0].get("name", "Unknown")
#             artist = "test"
#             yield score, recording_id, title, artist
#     except KeyError:
#         print("Errore nel parsing dei risultati AcoustID")

# def lookup_musicbrainz(recording_id):
#     # Cerca i dettagli del brano su MusicBrainz utilizzando il recording ID
#     try:
#         result = musicbrainzngs.get_recording_by_id(recording_id, includes=["artists", "releases"])
#         # Nome del file in cui vuoi scrivere il risultato
#         file_path = r"./result_output.txt"

#         # Scrivi il risultato su un file
#         with open(file_path, "w", encoding="utf-8") as file:
#             pprint.pprint(result, stream=file)

#         recording = result["recording"]
#         title = recording["title"]
#         artist = "test"
#         # artist = recording["artist-credit"][0]["name"]
#         album = recording.get("release-list", [{}])[0].get("title", "Unknown")
#         print(f"Track found:\ntitle: {title}\nartist: {artist}\nAlbum: {album}")
#     except musicbrainzngs.WebServiceError as e:
#         print(f"Errore nella ricerca su MusicBrainz: {e}")

# def identify_track(file_path):
#     recording_id = get_acoustic_id(file_path)
#     if recording_id:
#         lookup_musicbrainz(recording_id)

# # Esegui l'identificazione del file audio
# file_path = r"C:\Users\prora\Desktop\Anuel AA - China.mp3"#r"C:\Users\prora\Desktop\Music_library\server\media\Don Omar\Don Omar - Virtual Diva.mp3"
# identify_track(file_path)


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