from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.http import JsonResponse

import os
import traceback
import logging


#my lib
from .function import functions, query, error

#login
from django.contrib.auth import login
from .forms import  LoginUserForm
from django.contrib.auth import login, logout

#ChrmeDriver
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import googleapiclient.discovery
import pprint as pprint

import requests
from django.http import HttpResponse

logger = logging.getLogger(__name__)

def indexSlugless(request):

    if not request.user.is_authenticated:
        return redirect(reverse('login'))  # Redireziona usando il nome dell’UR

    return render(request, 'base.html')

def index(request, slug):

    #print("slug: ", slug)

    if not request.user.is_authenticated:
        return redirect(reverse('login'))  # Redireziona usando il nome dell’UR
    
    # Verifica se la richiesta è AJAX
    if request.headers.get("x-requested-with") == "XMLHttpRequest":

        match slug:

            case "brani":
                tracksROW = query.getTracks()
                tracks = []

                for track in tracksROW:
                    tracks.append([track[0], track[1], track[2], track[3], track[4], track[5], track[6]])

                data = {"tracks":tracks, "slug":slug}

                return render(request, 'indexBrani.html', data)
            
            case "album":
                albumsROW = query.getAlbums()
                # albums = []
                # for album in albumsROW:
                #     albums.append([album[0], album[1], album[2]])
                albums = albumsROW

                data = {"albums":albums, "slug":slug}

                return render(request, 'indexAlbum.html', data)
            
            case "artisti":
                
                artists = query.getArtists()

                data = {"artists":artists, "slug":slug}

                return render(request, 'indexArtisti.html', data)

    else:
        return render(request, 'base.html')

def artist_page(request, artist_slug):

    print("slug: ", artist_slug)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        data_artist = query.getArtist(artist_slug)

        # song_artist = query.getTracksArtist(artist_slug)

        result = query.getAllData(artist_slug)

        structured_data = {"albumProprietari": {}, "albumNonProprietari": {}}

        for entry in result:
            album_id = entry[0]
            traccia_id = entry[5]
            variant = entry[11]
            
            album_entry = {
                "album_nome": entry[1],
                "data_pubblicazione": entry[2],
                "artisti": [
                    {"artista_id": artist.split(',')[0], "artist_name": artist.split(',')[1]}
                    for artist in entry[3].split(';')
                ],
                "tracce": {}
            }

            traccia_entry = {
                "id": traccia_id,
                "titolo": entry[6],
                "autore": entry[7],
                "artisti_partecipanti": entry[8],
                "durata": entry[9],
                "file_name": entry[10],
            }

            # Verifica se l'album è proprietario o meno
            if entry[4]:  # Proprietario
                if album_id not in structured_data["albumProprietari"]:
                    structured_data["albumProprietari"][album_id] = album_entry

                # Aggiungi la traccia
                structured_data["albumProprietari"][album_id]["tracce"][f"{traccia_id}-{variant}"] = traccia_entry
            else:  # Non Proprietario
                if album_id not in structured_data["albumNonProprietari"]:
                    structured_data["albumNonProprietari"][album_id] = album_entry

                # Aggiungi la traccia
                structured_data["albumNonProprietari"][album_id]["tracce"][f"{traccia_id}-{variant}"] = traccia_entry

        # Stampa il risultato
        # import pprint
        # pprint.pprint(structured_data)

        context={"dataArtist": data_artist, "data":structured_data}

        return render(request, 'artista.html', context)

    else:
        return redirect('index-slugless')


def album_page(request, album_slug):

    print("slug: ", album_slug)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        album = query.getAlbum(album_slug)
        # pprint.pprint(album)

        tracks_row = query.getTrackFromAlbum(album_slug)
        # pprint.pprint(tracks)
        
        tracks = [
            {
                "track_id": track[0],
                "title": track[1],
                "artist": track[2],
                "album": track[3],
                "album_id": track[4],
                "duration": track[5],
                "file_path": track[6],
                "play_count": track[7],
            }
            for track in tracks_row
        ]
        

        context={"album": album, "tracks": tracks}

        return render(request, 'album.html', context)

    else:
        return redirect('index-slugless')
    

def search(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        # API information
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyD_-bYTsQkcImAuiXpyfEDnsQSijxy7s6c"
        # API client
        youtube = googleapiclient. discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
        # Request body
        #URl of VIdeo: https://www.youtube.com/watch?v=OwnsPhzZQEM
        youtube_request = youtube.search().list(
            part='snippet',
            q="lady gaga",
            maxResults=3,
            order="relevance",
            type="video",
            videoEmbeddable="true"
        )

        # Parametri Importanti:
        
        # part:
        # Specifica quali campi del risultato vuoi ottenere. In questo caso, snippet include informazioni come titolo, descrizione, miniature, canale, ecc.
        
        # q:
        # La query di ricerca, cioè il termine che vuoi cercare su YouTube. In questo esempio, stai cercando i video relativi a "Whistling Diesel".
        
        # maxResults:
        # Specifica il numero massimo di risultati da restituire (in questo caso, 3).
        
        # order:
        # Specifica come ordinare i risultati. In questo caso, "date" ordina i risultati dal più recente al più vecchio.
        
        # type:
        # Specifica il tipo di risorsa da cercare. Può essere:
        # "video": cerca solo video.
        # "channel": cerca solo canali.
        # "playlist": cerca solo playlist.
        # Qui hai scelto "video".

        youtube_response = youtube_request.execute()

        pprint.pprint(youtube_response)

        video_data = []
        for item in youtube_response["items"]:
            video_data.append({
                "video_id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                "published_at": item["snippet"]["publishedAt"],
            })


        return render(request, 'search.html', {"videos": video_data})
    
    else:
        return redirect('index-slugless')


def upload(request):
    
    context = {}

    if request.method == 'POST':
        # carico il file
        file = request.FILES.get('songFile')
        if file: 
            print(file.name)
            fssv = FileSystemStorage(settings.MEDIA_ROOT)
            fssv.save(file.name, file)  # Salva il file
            print("[uploading] ", file.name)

            try:
                variantCheckbox = request.POST.get("variantCheckbox")
                functions.uploadSongOnDB(os.path.join(settings.MEDIA_ROOT, file.name), file.name, variantCheckbox)
                # return JsonResponse({"message": Canzone caricata con successo!})
                context["message"] = "Canzone caricata con successo!"

            except error.TrackJustRegistred:
                context["message"] = "Traccia già registrata"
                os.remove(os.path.join(settings.MEDIA_ROOT, file.name))
            
            except error.AlbumServerTimeout:
                context["message"] = "Non è stato possibile recuperare l'immagine dell'album (timeout risposta dai server)"

            except error.NoAlbumImgFound:                
                # return JsonResponse({"message": "Non è stato possibile recuperare l'immagine dell'album"})
                context["message"] = "Non è stato possibile recuperare l'immagine dell'album (possibile che i server non l'abbiano fornita)"
            
            except error.NoArtistImgFound:
                # return JsonResponse({"message": "Non è stato possibile recuperare l'immagine dell'artista"})
                context["message"] = "Non è stato possibile recuperare l'immagine dell'artista"

            except Exception:
                # return JsonResponse({"message": "Errore durante il caricamento della canzone"})
                context["message"] = "Errore durante il caricamento della canzone"

    # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     return render(request, 'upload.html')  
    
    return render(request, 'upload.html', context)

def logIn(request):
    
    if request.method=='POST':
        form = LoginUserForm(data=request.POST)

        if form.is_valid():
            user=form.get_user()
            logger.info("Successfully logged for %s"%(user))
            #messages.success(request, "Logged successfully as %s"%(user))
            login(request, user)
            return redirect('index-slugless')

    else:
        form = LoginUserForm()

    return render(request, 'login.html', {"form": form})

def logOut(request):

    logout(request)
    logger.info("Successfully logout for %s"%(request.user))
    return redirect('home')