from django.conf import settings
from django.db import transaction
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static

import subprocess
import json
import os
import shutil
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.flac import FLAC
from mutagen.mp4 import MP4  # per file M4A
import traceback
import requests
import shutil
import logging

from . import deezerAPI
from . import lastFmAPI
from . import musicBrainzAPI as mdAPI
from ..query import *
from .error import *
from .acusticid import *

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
        
    def getJsonMetadata(self):
        dict = {}
        for key, value in self.audio.items():
            dict[key]=value

        return dict

    def pritnMetadata(self):
        if self.audio:
            print("[MUTAGEN]")
            for key, value in self.audio.items():
                print(f"{key}: {value}")
            return dict(self.audio)  # Restituisci i metadati come dizionario, se necessario
        else:
            print("Nessun metadato disponibile.")
            return None


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

    msg_return = []

    # reg !var -> exception
    # reg var -> incremento variant
    # !reg !var -> inserimento normale
    # !reg var -> set variant to 1

    idTrack = None
    idAlbum = None

    try:
        with transaction.atomic():
            # lettura metadati
            try:
                mutagenIstance = MutagenClass(filePath)
                idTrack = mutagenIstance.getIDtrack()
                idAlbum = mutagenIstance.getIDalbum()
                logger.debug(f"Metadati traccia estratti offline: {mutagenIstance.getJsonMetadata()}") # non viene stampato
            except HeaderNotFoundError:
                logger.warning("Non è stato possibile estrapolare le informazione dal file provo con Acustic ID")
                # fingerprint = get_acoustic_id(filePath)
                # print("AAAAAAAAA: ", lookup_musicbrainz(fingerprint))
                result = get_song_data(filePath)
                print("acusticID: ", result)
                idTrack = result["recording_id"]
                idAlbum = result["album_id"]


            print("id: ", idTrack)
            if idTrack == None:
                pass
            
            # leggere il nome e vedere se contiene sloweed....
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

            if idAlbum == None:
                mdAPI.getMetadataByTitleAndArtist() ####################################àPARAM TITLE
            # logger.debug("ID album: ", idAlbum)
            print("album: ", idAlbum)

            OnlineTrackMetadata = mdAPI.getMetadataByrecordingID(idTrack)
            print("[OnlineTrackMetadata] ", OnlineTrackMetadata, "\n[OnlineTrackMetadata END]")

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

                    os.makedirs(os.path.join(settings.MEDIA_ROOT, dataArtist["name"]), exist_ok=True) #se esiste
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
                logger.info(f"Album {OnlineAlbumMetadata['title']}:{idAlbum} non registrato")

                registerAlbum(idAlbum, OnlineAlbumMetadata["title"], OnlineAlbumMetadata["date"])
                try:
                    download_album_img(idAlbum) #null con billie elish
                # except AlbumServerTimeout:
                #     raise AlbumServerTimeout
                # except NoAlbumImgFound:
                #     msg_return.append("Nessun immagine trovata, immagine default impostata")
                except Exception as e:

                    logger.error(f"{e}")

                    source = os.path.join(settings.STATIC_ROOT, "icone", "default_cover.jpg")
                    # source = staticfiles_storage.path('icone/default_cover.jpg')
                    # source = static('icone/default_cover.jpg')
                    print("debuggg:::", source)

                    # Percorso del file di destinazione
                    destination = os.path.join(settings.MEDIA_ROOT, "Album", f"{idAlbum}.jpg")

                    try:
                        # Copia del file
                        shutil.copy(source, destination)
                        print(f"File copiato con successo da {source} a {destination}")
                        msg_return.append("Errore durante il download dell'immagine dell'album, immagine default impostata")
                    except FileNotFoundError:
                        logger.error(f"Il file sorgente a {source} non esiste!")
                    except PermissionError:
                        logger.error("Permesso negato! Controlla i permessi del file o della cartella.")
                    except Exception as e2:
                        logger.error(f"Errore durante la copia del file: {e2}")

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

    # except TrackJustRegistred:
    #     logger.warning("Traccia gia registrata")
    #     raise TrackJustRegistred
                
    except Exception as error:
        
        logger.error(traceback.format_exc())
        traceback.print_exc()
        
        raise error