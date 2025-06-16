# from django.db import connection
# from datetime import datetime

# def isTrackRegistred(idTrack):
    
#     try:
#         query = "SELECT id FROM traccia WHERE id=%s"
#         with connection.cursor() as cursor:
#             cursor.execute(query, (idTrack, ))
#             result = cursor.fetchone()

#             if result:
#                 return True
#             else:
#                 return False
            
#     except Exception as error:
#         raise error
    
# def getVariantNum(idTrack):

#     try:
#         query = "SELECT variant FROM traccia WHERE id=%s"
#         with connection.cursor() as cursor:
#             cursor.execute(query, (idTrack, ))
#             return cursor.fetchone()[0]
            
#     except Exception as error:
#         raise error

# def registerTrack(idTraccia, titolo, autore, artisti, idAlbum, durata, fileName, variant):

#     try:
#         query = "INSERT INTO traccia VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#         with connection.cursor() as cursor:
#             cursor.execute(query, (idTraccia, titolo, autore, artisti, idAlbum, durata, fileName, variant, ))
#     except Exception as error:
#         raise error

# def isArtistRegistred(id):

#     try:
#         query = "SELECT id FROM artista WHERE id=%s"
#         with connection.cursor() as cursor:
#             cursor.execute(query, (id, ))
#             result = cursor.fetchone()

#             print("[result of isArtistRegistred] ", result)

#             if result:
#                 return True
#             else:
#                 return False
            
#     except Exception as error:
#         raise error
        
# def registerArtist(id, country, artist_name, descrizione):
    
#     try:
#         query = "INSERT INTO artista VALUES (%s, %s, %s, %s)"
#         with connection.cursor() as cursor:
#             cursor.execute(query, (id, country, artist_name, descrizione, ))
#     except Exception as error:
#         raise error

# def isAlbumRegistred(albumID):
#     try:
#         query = "SELECT id FROM album WHERE id=%s"
#         with connection.cursor() as cursor:
#             cursor.execute(query, (albumID, ))
#             result = cursor.fetchone()

#             if result:
#                 return True
#             else:
#                 return False
            
#     except Exception as error:
#         raise error

# def registerAlbum(id, nome, data):
#     try:

#         # Trasforma `data` in un oggetto datetime.date, se non lo è già
#         # if isinstance(data, str):
#         #     data = datetime.strptime(data, '%Y-%m-%d').date()
#         # elif isinstance(data, datetime):
#         #     data = data.date()  # Se `data` è datetime, prendiamo solo la parte di data

#         query = "INSERT INTO album VALUES (%s, %s, %s)"
#         with connection.cursor() as cursor:
#             cursor.execute(query, (id, nome, data, ))
#     except Exception as error:
#         raise error

# def isAlbum_ArtistRegistred(artistID, AlbumID):
#     try:
#         query = "SELECT * FROM artista_album WHERE artista_id=%s AND album_id=%s"
#         with connection.cursor() as cursor:
#             cursor.execute(query, (artistID, AlbumID, ))
#             result = cursor.fetchone()

#             if result:
#                 return True
#             else:
#                 return False
            
#     except Exception as error:
#         raise error

# def registerArtistAlbum(artistaID, albumID, owner):
    
#     try:

#         # Assicura che `owner` sia un booleano
#         if not isinstance(owner, bool):
#             raise ValueError("Il parametro 'owner' deve essere di tipo booleano.")
        
#         query = "INSERT INTO artista_album VALUES (%s, %s, %s)"
#         with connection.cursor() as cursor:
#             cursor.execute(query, (artistaID, albumID, owner, ))
#     except Exception as error:
#         raise error

# def getArtists():

#     try:
#         query = "SELECT * FROM artista"
#         with connection.cursor() as cursor:
#             cursor.execute(query)
#             return cursor.fetchall()

#     except Exception as error:
#         raise error

# def getArtist(id: str):

#     try:
#         query = "SELECT * FROM artista WHERE id = %s"
#         with connection.cursor() as cursor:
#             cursor.execute(query, (id, ))
#             result = cursor.fetchone()
        
#         result = {
#             'id': result[0],
#             'country': result[1],
#             'name': result[2],
#             'descrizione': result[3]
#         }

#         return result

#     except Exception as error:
#         raise error

# def getAlbums():

#     try:
#         query = "SELECT * FROM album"
#         with connection.cursor() as cursor:
#             cursor.execute(query)
#             return cursor.fetchall()

#     except Exception as error:
#         raise error
    
# def getTrackFromAlbum(id_album):

#     try:
#         query = """
#             SELECT * 
#             FROM traccia
#             WHERE album_id = %s;
#             """
#         with connection.cursor() as cursor:
#             cursor.execute(query, (id_album, ))
#             return cursor.fetchall()

#     except Exception as error:
#         raise error 

# def getAlbum(id_album):

#     try:
#         query = """
#             SELECT * 
#             FROM album
#             WHERE id = %s;
#             """
#         with connection.cursor() as cursor:
#             cursor.execute(query, (id_album, ))
#             result = cursor.fetchone()

#             result = {
#             'id': result[0],
#             'nome': result[1],
#             'data': result[2]
#             }

#         return result

#     except Exception as error:
#         raise error
    

# def getTracks():

#     try:
#         query = "SELECT * FROM traccia"
#         with connection.cursor() as cursor:
#             cursor.execute(query)
#             return cursor.fetchall()

#     except Exception as error:
#         raise error

# def getTracksArtist(idArtist: str):

#     try:
#         query = "\
#             SELECT * FROM traccia  \
#             WHERE album_id IN \
#             ( \
# 	            SELECT album_id FROM artista_album\
# 	            WHERE artista_id = %s AND proprietario = true\
#             )"
        
#         with connection.cursor() as cursor:
#             cursor.execute(query, (idArtist, ))
#             result =  cursor.fetchall()
        
#         result = [
#         {
#             'id': row[0],
#             'titolo': row[1],
#             'autore': row[2],
#             'artistParticipants': row[3],
#             'album_id': row[4],
#             'durata': row[5],
#             'fileName': row[6]
#         }
#         for row in result
#         ]

#         return result

#     except Exception as error:
#         raise error
    
# def getAllTracksArtist(idArtist: str):

#     try:
#         query = "\
#             SELECT * FROM traccia  \
#             WHERE album_id IN \
#             ( \
# 	            SELECT album_id FROM artista_album\
# 	            WHERE artista_id = %s\
#             )"
        
#         with connection.cursor() as cursor:
#             cursor.execute(query, (idArtist, ))
#             return cursor.fetchall()

#     except Exception as error:
#         raise error

# def getAllData(idArtist: str):

#     try:
#         query = """
#             SELECT 
#                 AA.album_id AS album_id,
#                 A.nome AS album_nome,
#                 A.data AS data_pubblicazione,
#                 STRING_AGG(AA.artista_id::text || ',' || Ar.artist_name, ';') AS artista,
#                 AA.proprietario AS proprietario,
#                 T.id,
#                 T.titolo,
#                 T.autore,
#                 T.artisti_partecipanti,
#                 T.durata,
#                 T.file_name,
#                 T.variant
#             FROM 
#                 album AS A
#             JOIN 
#                 artista_album AS AA ON A.id = AA.album_id
#             JOIN 
#                 traccia AS T ON A.id = T.album_id
#             JOIN 
#                 artista AS Ar ON AA.artista_id = Ar.id
#             WHERE 
#                 AA.artista_id = %s
#             GROUP BY 
#                 AA.album_id, A.nome, A.data, AA.proprietario, T.id, T.titolo, T.autore, T.artisti_partecipanti, T.durata, T.file_name, T.variant
#         """

#         with connection.cursor() as cursor:
#             cursor.execute(query, (idArtist, ))
#             result = cursor.fetchall()

#             return result

#     except Exception as error:
#         raise error


## -- ORM --

from django.db import IntegrityError, transaction
# from django.template.defaultfilters import slugify
from django.db.models import Exists, OuterRef
from django.db.models.functions import Cast
from django.contrib.postgres.aggregates import StringAgg

from .models import Track as Traccia, Artist as Artista, Album, ArtistAlbum

def isTrackRegistred(idTrack):
    return Traccia.objects.filter(id=idTrack).exists()

def getVariantNum(idTrack):
    tr = Traccia.objects.get(id=idTrack)
    return tr.variant

def registerTrack(idTraccia, titolo, autore, artisti, idAlbum, durata, fileName, variant):
    """
    Crea una nuova traccia nel DB usando i nomi dei campi esatti del modello Track.
    """
    Traccia.objects.create(
        id=idTraccia,
        title=titolo,                            # <— title al posto di titolo
        author=autore,                            # <— author al posto di autore
        participating_artists=artisti,            # <— participating_artists
        album_id=idAlbum,                         # <— album_id (foreign key)
        duration=durata,                          # <— duration al posto di durata
        file_name=fileName,                       # <— file_name rimane invariato
        variant=variant                           # <— variant rimane invariato
        # play_count rimane al default = 0
    )

def isArtistRegistred(id):
    return Artista.objects.filter(id=id).exists()

def registerArtist(id, country, artist_name, descrizione):
    Artista.objects.create(
        id=id,
        country=country,
        name=artist_name,
        description=descrizione,
    )

def isAlbumRegistred(albumID):
    return Album.objects.filter(id=albumID).exists()

def registerAlbum(id, nome, data):
    Album.objects.create(
        id=id,
        title=nome,
        release_date=data
    )

def isAlbum_ArtistRegistred(artistID, albumID):
    # sfrutta il related_name 'artisti' su Album.artisti
    return ArtistAlbum.objects.filter(
        artist_id=artistID,
        album_id=albumID
    ).exists()

def registerArtistAlbum(artistaID, albumID, owner):
    """
    Crea una riga in artista_album tra l'artista e l'album, 
    ignorando il duplicate key error se la relazione esiste già.
    """
    try:
        with transaction.atomic():
            ArtistAlbum.objects.create(
                artist_id=artistaID,
                album_id=albumID,
                owner=owner
            )
    except IntegrityError:
        # La relazione esiste già (unique_together), la ignoriamo
        pass

def getArtists():
    return list(Artista.objects.values('id', 'country', 'name', 'description'))

def getArtist(id: str):
    return Artista.objects.filter(id=id) \
        .values('id', 'country', 'name', 'description') \
        .first()

def getAlbums():
    return list(Album.objects.values('id', 'title', 'release_date'))

def getTrackFromAlbum(id_album):
    qs = Traccia.objects.filter(album_id=id_album)
    return list(qs.values(
        'id', 'title', 'author', 'participating_artists',
        'album_id', 'duration', 'file_name', 'variant'
    ))

def getAlbum(id_album):
    return Album.objects.filter(id=id_album) \
        .values('id', 'title', 'release_date') \
        .first()

def getTracks():
    return list(Traccia.objects.values(
        'id', 'title', 'author', 'participating_artists',
        'album_id', 'duration', 'file_name', 'variant'
    ))

def getTracksArtist(idArtist: str):
    qs = Traccia.objects.filter(
        album__artistalbum__artist_id=idArtist,
        album__artistalbum__owner=True
    )
    return list(qs.values(
        'id', 'title', 'author', 'participating_artists',
        'album_id', 'duration', 'file_name', 'variant'
    ))

def getAllTracksArtist(idArtist: str):
    qs = Traccia.objects.filter(album__artistalbum__artist_id=idArtist)
    return list(qs.values(
        'id', 'title', 'author', 'participating_artists',
        'album_id', 'duration', 'file_name', 'variant'
    ))

def getAllData(idArtist: str):
    """
    Riproduci la tua query con un annotate+StringAgg:
    """
    qs = Album.objects.filter(artisti__id=idArtist) \
        .annotate(
            artista=StringAgg(
                Cast('artisti__id', output_field=models.TextField())
                + ',' + 'artisti__artist_name',
                delimiter=';'
            ),
            proprietario=OuterRef('artisti__through__proprietario')
        ) \
        .prefetch_related('traccia_set')

    result = []
    for alb in qs:
        for tr in alb.traccia_set.all():
            result.append({
                'album_id': alb.id,
                'album_nome': alb.titolo,
                'data_pubblicazione': alb.data_pubblicazione,
                'artista': alb.artista,
                'proprietario': alb.proprietario,
                'id': tr.id,
                'titolo': tr.titolo,
                'autore': tr.autore,
                'artisti_partecipanti': tr.artisti_partecipanti,
                'durata': tr.durata,
                'file_name': tr.file_name,
                'variant': tr.variant,
            })
    return result
