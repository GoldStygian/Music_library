# views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import os

from . import query

from .models import Artist, Album, Track
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from .function import functions, error

# Permessi: utenti autenticati per creare/modificare, tutti possono leggere
class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated



class ArtistViewSet(viewsets.ModelViewSet):

    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        uuid_value = kwargs.get(self.lookup_field)
        print("[d] uuid:", uuid_value)
        return super().retrieve(request, *args, **kwargs)



class AlbumViewSet(viewsets.ModelViewSet):
    """
    ViewSet per CRUD di Album.
    """
    queryset = Album.objects.prefetch_related('artistalbum_set__artist').all()
    serializer_class = AlbumSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]


# Aggiorna il ViewSet per usare il service
class TrackViewSet(viewsets.ModelViewSet):

    queryset = Track.objects.select_related('album').all()
    serializer_class = TrackSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):

            print("POST keys:", request.POST.keys())
            print("FILES keys:", request.FILES.keys())
            print("FILES list:", {k: len(v) for k, v in request.FILES.lists()})

            # Recupera i file e il campo variant dalla richiesta
            files = request.FILES.getlist('files')
            variant = request.POST.get('variant', 'false').lower() == 'true'  # Default a False se non presente
            # Verifica che ci sia almeno un file
            if not files:
                return Response({"error": "Nessun file caricato"}, status=status.HTTP_400_BAD_REQUEST)

            # Processa ogni file e raccogli i risultati
            results = []
            for file in files:
                # Salva temporaneamente il file
                fssv = FileSystemStorage(settings.MEDIA_ROOT)
                file_name = fssv.save(file.name, file)
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                print("FILE PATH: ", file_path)

                try:
                    functions.uploadSongOnDB(file_path, file.name, variant) # Chiama la funzione per caricare la traccia nel database
                    message = f"[{file.name}] Canzone caricata con successo!"
                    # fai lo spostamento qui del file
                except error.TrackJustRegistred:
                    # os.remove(file_path)
                    fssv.delete(file_name)
                    message = f"[{file.name}] Traccia già registrata"
                except Exception as e:
                    # os.remove(file_path)
                    fssv.delete(file_name)
                    message = f"[{file.name}] Errore durante il caricamento: {str(e)}"

                results.append({"file": file.name, "message": message})

            # Restituisci i risultati
            return Response(results, status=status.HTTP_201_CREATED)