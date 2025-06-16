# serializers.py
from rest_framework import serializers
from .models import Track, Album, Artist, ArtistAlbum

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'description']

class AlbumSerializer(serializers.ModelSerializer):
    # recupera gli artisti tramite il through model
    artists = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ['id', 'title', 'release_date', 'artists']

    def get_artists(self, obj):
        # restituisce lista di ArtistSerializer solo per i proprietari
        rels = ArtistAlbum.objects.filter(album=obj, owner=True)
        artists = [rel.artist for rel in rels]
        return ArtistSerializer(artists, many=True).data

class TrackSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True)
    variant = serializers.IntegerField(write_only=True, required=False, default=1)

    class Meta:
        model = Track
        # includi solo i campi effettivi del modello
        fields = [
            'id', 'title', 'author', 'participating_artists',
            'album', 'album_id', 'duration', 'file_name',
            'variant', 'play_count'
        ]
        read_only_fields = ['id', 'play_count']