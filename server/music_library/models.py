from django.db import models

import uuid
from django.db import models
# from django.utils.text import slugify

class Album(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    release_date = models.CharField(max_length=100, blank=True, null=True)
    
    # slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        db_table = 'album'

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Artist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    # slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        db_table = 'artista'

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ArtistAlbum(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, db_column='artista_id')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, db_column='album_id')
    owner = models.BooleanField(db_column='proprietario')

    class Meta:
        db_table = 'artista_album'
        unique_together = (('artist', 'album'),)


class Track(models.Model):
    VARIANT_CHOICES = [(i, str(i)) for i in range(1, 11)]  # adjust as needed

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, db_column='titolo')
    author = models.CharField(max_length=100, db_column='autore')
    participating_artists = models.CharField(max_length=255, blank=True, null=True, db_column='artisti_partecipanti')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, db_column='album_id')
    duration = models.CharField(max_length=100, blank=True, null=True, db_column='durata')
    file_name = models.TextField(blank=False, null=False, db_column='file_name')
    variant = models.IntegerField(choices=VARIANT_CHOICES, db_column='variant')
    play_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'traccia'
        unique_together = (('id', 'variant'),)

    # def save(self, *args, **kwargs):
    #     # store original filename if file is set
    #     if self.file and not self.file_name:
    #         self.file_name = self.file.name
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.variant})"
