from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

import os
import traceback
import logging

from .function import functions, query

logger = logging.getLogger(__name__)

#login
from django.contrib.auth import login
from .forms import  LoginUserForm
from django.contrib.auth import login, logout

def indexSlugless(request):
    return index(request, "album")

def index(request, slug):

    print("slug: ", slug)

    if not request.user.is_authenticated:
        return redirect(reverse('login'))  # Redireziona usando il nome dell’UR

    if request.method == 'POST':

        #carico il video
        file = request.FILES.get('songFile')
        if file: 
            file = request.FILES['songFile']
            print(file.name)

            fssv = FileSystemStorage(settings.MEDIA_ROOT)
            fssv.save(file.name, file)#qui è possibile ridenominare il file prima di caricarlo
            print("[uploading] ", file.name)
            
            try:
                functions.uploadSongOnDB(os.path.join(settings.MEDIA_ROOT, file.name), file.name)
            except Exception:
                traceback.print_exc()
                os.remove(os.path.join(settings.MEDIA_ROOT, file.name))
    
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

    # match slug:

    #     case "album":

    #         albumsROW = query.getAlbums()
    #         albums = []
    #         for album in albumsROW:
    #             albums.append([album[0], album[1], album[2]])

    #         data = {"albums":albums, "slug":slug}

    #         template_name = 'indexAlbum.html' if is_ajax else 'base.html'
    #         return render(request, template_name, data)
        
    #     case "brani":

    #         tracksROW = query.getTracks()
    #         tracks = []
    #         print(tracksROW)
    #         for track in tracksROW:
    #             tracks.append([track[0], track[1], track[2], track[3], track[4], track[5], track[6]])

    #         data = {"tracks":tracks, "slug":slug}

    #         template_name = 'indexBrani.html' if is_ajax else 'index.html'
    #         return render(request, template_name, data)

from django.db import connection
def artist_page(request, artist_slug):

    print("sluuuuuuuug ", artist_slug)

    dataArtist = query.getArtist(artist_slug)

    songArtist = query.getTracksArtist(artist_slug)

    result = query.getAllData(artist_slug)

    print(type(result[0][4]))

    structured_data = {"albumProprietari": {}, "albumNonProprietari": {}}

    for entry in result:
        album_id = entry[0]
        traccia_id = entry[5]
        
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
            structured_data["albumProprietari"][album_id]["tracce"][traccia_id] = traccia_entry
        else:  # Non Proprietario
            if album_id not in structured_data["albumNonProprietari"]:
                structured_data["albumNonProprietari"][album_id] = album_entry

            # Aggiungi la traccia
            structured_data["albumNonProprietari"][album_id]["tracce"][traccia_id] = traccia_entry

    # Stampa il risultato
    import pprint
    pprint.pprint(structured_data)

    context={"dataArtist": dataArtist, "data":structured_data}

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'artista.html', context)

@csrf_exempt
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