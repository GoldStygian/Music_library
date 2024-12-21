from django.conf import settings
from django.db import transaction

import subprocess
import json
import os
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4  # per file M4A
import traceback
import requests
import shutil
import logging

from . import deezerAPI
from . import lastFmAPI
from . import musicBrainzAPI as mdAPI
from .query import *
from .error import *

logger = logging.getLogger(__name__)

def download_image(image_url, filePath):

    os.path.normpath(filePath)

    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filePath, 'wb') as handler:
            handler.write(response.content)
        print("Immagine scaricata con successo.")
    else:
        print("Errore nel download dell'immagine.")


class MutagenClass:

    class InvalidFileType(Exception):
        def __init__(self, message):
            super().__init__(message)  # Chiama il costruttore della classe base
            self.message = message  # Memorizza il messaggio di errore
    
    class InvalidInitialization(Exception):
        def __init__(self, message):
            super().__init__(message)  # Chiama il costruttore della classe base
            self.message = message  # Memorizza il messaggio di errore

    def __init__(self, filePath):

        if filePath.endswith(".mp3"):
            self.audio = MP3(filePath, ID3=EasyID3)
        elif filePath.endswith(".flac"):
            self.audio = FLAC(filePath)
        elif filePath.endswith(".m4a") or filePath.endswith(".mp4"):
            self.audio = MP4(filePath)
        else:
            raise self.InvalidFileType("[-] can't handel this file")

        if self.audio is None:
            raise self.InvalidInitialization("[-] error during initiaòlization or t")


    def getIDtrack(self):

        if "musicbrainz_trackid" in self.audio:
            return self.audio["musicbrainz_trackid"][0]
        else:
            return None
        
    def getIDalbum(self):

        if "musicbrainz_albumid" in self.audio:
            return self.audio["musicbrainz_albumid"][0]
        else:
            return None
        
    def getTitleTrack(self):

        if "title" in self.audio:
            return self.audio["title"][0]
        else:
            return None
    
    def getDurationTrack(self):
            
        if "length" in self.audio:
            minuti = int(int(self.audio["length"][0])/1000/60)
            secondi = int((int(self.audio["length"][0])/1000)%60)
            if secondi < 10 and secondi > 0:
                secondi = f"0{secondi}"

            return f"{minuti}:{secondi}"
        
        else:
            return None

    def getArtistTrack(self):
        
        if "artist" in self.audio:
            return self.audio["artist"][0]
        else:
            return None

    def getAllMetadata(self):
        return self.audio


def getJsonMetadata(filePath):

    # Comando ffprobe per ottenere tutti i metadati
    result = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-show_format', '-show_streams', filePath],
        #['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filePath],
        stdout=subprocess.PIPE,
        text=True
    )
    metadata = json.loads(result.stdout)
    return metadata


def download_artist_img(artistID, artistName):

    image_url = deezerAPI.get_artist_image_from_deezer(artistName) or lastFmAPI.get_artist_image_from_lastfm(artistID, settings.LAST_FM_API_KEY)
    if image_url:
        download_image(image_url, os.path.join(settings.MEDIA_ROOT, f"{artistName}/cover.jpg"))
    else:
        raise NoArtistImgFound
    
def download_album_img(albumID):
    
    data = mdAPI.getCoverAlbumByAlbumID(albumID) #null con billie elish
    if data:
        print("donloading: ", data["images"][0]["image"])
        try:
            download_image(data["images"][0]["image"], settings.MEDIA_ROOT+rf"/Album/{albumID}.jpg")
        except requests.exceptions.Timeout:
            raise AlbumServerTimeout
    else:
        raise NoAlbumImgFound

def extractArtist(artistsRow):

    #estraggo gli estisti dalla stringa ROW
    ignore_words = {"feat.", "feat", "featuring", "&"}

    #found_words = artistsRow.split()

    # Dividi le parole tra artisti e parole ignorate
    #found_artists = [word for word in found_words if word.lower() not in ignore_words]
    #found_ignored = [word for word in found_words if word.lower() in ignore_words]
    
    ignored_words = []  # Lista per memorizzare le parole ignorate
    # Creiamo un pattern per separare gli artisti dalle parole ignorate
    for word in ignore_words:
        if word in artistsRow:  # Controlla se la parola ignorata è presente
            ignored_words.extend([word] * artistsRow.count(word))  # Aggiungi alla lista in base al numero di occorrenze
            artistsRow = artistsRow.replace(word, ",")  # Sostituisci le parole ignorate con una virgola
    
    # Ora possiamo dividere la stringa sulla base della virgola
    found_artists = [artist.strip() for artist in artistsRow.split(',') if artist.strip()]
    
    print(f"[Artisti trovati]: {found_artists}, Parole ignorate: {ignored_words}")

    return [found_artists, found_artists]


def uploadSongOnDB(filePath, fileName, variant):

    logger.info(f"Caricando {fileName}")

    # reg !var -> exception
    # reg var -> incremento variant
    # !reg !var -> inserimento normale
    # !reg var -> set variant to 1

    try:
        with transaction.atomic():
            # lettura metadati
            mutagenIstance = MutagenClass(filePath)
            logger.debug(f"Metadati traccia estratti offline: {mutagenIstance.getAllMetadata()}")
            #print("[song metadata]\n", json.dumps(MutagenMetadata, indent=4, sort_keys=True))

            # artists = extractArtist(metadata["format"]["tags"]["artist"]) # metadata["format"]["tags"]["artist"] # puo contenere &, feturing, feat.

            idTrack = mutagenIstance.getIDtrack()
            # logger.debug("ID traccia: ", idTrack)
            print("id: ", idTrack)
            
            n_variant = 0
            if isTrackRegistred(idTrack): 

                if variant: # reg var
                    n_variant = getVariantNum(idTrack) + 1

                else: #reg !var
                    raise TrackJustRegistred
                
            else:
                
                if variant:
                    n_variant = getVariantNum(idTrack) + 1

                else:
                    n_variant = 0     



            idAlbum = mutagenIstance.getIDalbum()
            # logger.debug("ID album: ", idAlbum)
            print("album: ", idAlbum)

            OnlineTrackMetadata = mdAPI.getMetadataByrecordingID(idTrack)
            logger.debug(f"Metadati traccia estratti trmite API: {json.dumps(OnlineTrackMetadata, indent=4, sort_keys=True)}")

            firtArtist = None
            listArtist = ""

            for data in OnlineTrackMetadata["artist-credit"]:          
            
                artistID = data["artist"]["id"]

                if firtArtist==None:
                    firtArtist = data["name"]
                    listArtist = data["name"]
                else:
                    listArtist += f";{data["name"]}"

                if not isArtistRegistred(artistID):
                    logger.info(f"Artista {data["name"]}:{artistID} non registrato")
                    
                    dataArtist = mdAPI.getMetadataByArtistID(artistID)
                    
                    description = lastFmAPI.get_artist_description_from_lastfm(artistID, settings.LAST_FM_API_KEY)

                    # registerArtist(artistID, dataArtist["area"]["name"], dataArtist["name"], description if description else "")
                    registerArtist(artistID, dataArtist["area"]["name"], dataArtist["name"], description)

                    os.mkdir(os.path.join(settings.MEDIA_ROOT, dataArtist["name"])) #se esiste
                    download_artist_img(artistID, dataArtist["name"])
                else:
                    logger.info(f"Artista {data["name"]}:{artistID} gia registrato")
            
            logger.debug("Metadati traccia estratti trmite API (SUCCESS)")


            # album
            # - artista ID 
            OnlineAlbumMetadata = mdAPI.getMetadataByAlbumID(idAlbum)
            logger.debug(f"Metadati album estratti trmite API: {json.dumps(OnlineAlbumMetadata, indent=4, sort_keys=True)}")

            # registro l'album
            if not isAlbumRegistred(idAlbum):
                logger.info(f"Album {OnlineAlbumMetadata["title"]}:{idAlbum} non registrato")

                registerAlbum(idAlbum, OnlineAlbumMetadata["title"], OnlineAlbumMetadata["date"])
                try:
                    download_album_img(idAlbum) #null con billie elish
                except AlbumServerTimeout:
                    raise AlbumServerTimeout
                except NoAlbumImgFound:
                    raise NoAlbumImgFound
            else:
                logger.info(f"Album {OnlineAlbumMetadata["title"]}:{idAlbum} gia registrato")


            # registro le associazioni proprietarie gli album
            for data in OnlineAlbumMetadata["artist-credit"]: #inserendo gli artisti dell'album (non per forza hanno tracce)
                artistID = data["artist"]["id"]
                if not isArtistRegistred(artistID):

                    description = lastFmAPI.get_artist_description_from_lastfm(artistID, settings.LAST_FM_API_KEY)
                    registerArtist(data["artist"]["id"], None, data["artist"]["name"], description)
                    os.mkdir(os.path.join(settings.MEDIA_ROOT, data["artist"]["name"])) #se esiste
                    
                    try:
                        download_artist_img(artistID, data["artist"]["name"])
                    except NoArtistImgFound:
                        raise NoArtistImgFound
                    
                if not isAlbum_ArtistRegistred(data["artist"]["id"], idAlbum):
                    registerArtistAlbum(data["artist"]["id"], idAlbum, True)

            logger.debug("Metadati album estratti trmite API (SUCCESS)")

            #registro gli artisti
            for data in OnlineTrackMetadata["artist-credit"]:

                if not isAlbum_ArtistRegistred(data["artist"]["id"], idAlbum):
                    registerArtistAlbum(data["artist"]["id"], idAlbum, False)

            # spostare il file nel primo artista che compare
            shutil.move(filePath, os.path.join(settings.MEDIA_ROOT, firtArtist))

            # registro la traccia
            registerTrack(idTrack, mutagenIstance.getTitleTrack(), mutagenIstance.getArtistTrack(), listArtist ,idAlbum, mutagenIstance.getDurationTrack(), f"{firtArtist}/{fileName}", n_variant)

            logger.info(f"Caricamneto di {fileName} completato con successo")

            return {"id_track": idTrack, "id_album": idAlbum, "id_artist": firtArtist}

    except TrackJustRegistred:
        logger.warning("Traccia gia registrata")
        raise TrackJustRegistred
                
    except Exception as error:
        logger.error(traceback.format_exc())
        # rollback del DB (gestito da django)
        
        # rollback file
        os.remove(os.path.join(settings.MEDIA_ROOT, filePath))
        
        raise error


"""
OnlineAlbumMetadata
 {
    "artist-credit": [
        {
            "artist": {
                "disambiguation": "",
                "id": "302bd7b9-d012-4360-897a-93b00c855680",
                "name": "David Guetta",
                "sort-name": "Guetta, David",
                "type": "Person",
                "type-id": "b6e035f4-3ce9-331c-97df-83397230b0df"
            },
            "joinphrase": " & ",
            "name": "David Guetta"
        },
        {
            "artist": {
                "disambiguation": "Australian singer\u2010songwriter",
                "id": "2f548675-008d-4332-876c-108b0c7ab9c5",
                "name": "Sia",
                "sort-name": "Sia",
                "type": "Person",
                "type-id": "b6e035f4-3ce9-331c-97df-83397230b0df"
            },
            "joinphrase": "",
            "name": "Sia"
        }
    ],
    "asin": null,
    "barcode": null,
    "country": "GB",
    "cover-art-archive": {
        "artwork": true,
        "back": false,
        "count": 1,
        "darkened": false,
        "front": true
    },
    "date": "2018-03-22",
    "disambiguation": "",
    "id": "69307f05-6182-4d73-bfad-0e11346b526f",
    "packaging": "None",
    "packaging-id": "119eba76-b343-3e02-a292-f0f00644bb9b",
    "quality": "normal",
    "release-events": [
        {
            "area": {
                "disambiguation": "",
                "id": "8a754a16-0027-3a29-b6d7-2b40ea0481ed",
                "iso-3166-1-codes": [
                    "GB"
                ],
                "name": "United Kingdom",
                "sort-name": "United Kingdom",
                "type": null,
                "type-id": null
            },
            "date": "2018-03-22"
        }
    ],
    "status": "Official",
    "status-id": "4e304316-386d-3409-af2e-78857eec5cfe",
    "text-representation": {
        "language": "eng",
        "script": "Latn"
    },
    "title": "Flames"
}"""

"""
{
  "packaging": "Jewel Case",
  "status": "Official",
  "quality": "normal",
  "packaging-id": "ec27701a-4a22-37f4-bfac-6616e0f9750a",
  "barcode": "9397604000569",
  "disambiguation": "",
  "country": "AU",
  "cover-art-archive": {
    "count": 0,
    "darkened": false,
    "back": false,
    "front": false,
    "artwork": false
  },
  "title": "7",
  "asin": null,
  "status-id": "4e304316-386d-3409-af2e-78857eec5cfe",
  "artist-credit": [
    {
      "artist": {
        "name": "David Guetta",
        "sort-name": "Guetta, David",
        "id": "302bd7b9-d012-4360-897a-93b00c855680",
        "type-id": "b6e035f4-3ce9-331c-97df-83397230b0df",
        "disambiguation": "",
        "type": "Person"
      },
      "name": "David Guetta",
      "joinphrase": ""
    }
  ],
  "id": "f88f6bd5-3d75-4a51-843a-f020312fd3f0",
  "date": "2018-09-14",
  "release-events": [
    {
      "date": "2018-09-14",
      "area": {
        "iso-3166-1-codes": [
          "AU"
        ],
        "type-id": null,
        "id": "106e0bec-b638-3b37-b731-f53d507dc00e",
        "sort-name": "Australia",
        "name": "Australia",
        "type": null,
        "disambiguation": ""
      }
    }
  ],
  "text-representation": {
    "script": "Latn",
    "language": "eng"
  }
}"""