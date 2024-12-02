from django.db import connection
from datetime import datetime

# NOTE
# nessuna insert ritorna un risultato

def isTrackRegistred(idTrack):
    
    try:
        query = "SELECT id FROM traccia WHERE id=%s"
        with connection.cursor() as cursor:
            cursor.execute(query, (idTrack, ))
            result = cursor.fetchone()

            if result:
                return True
            else:
                return False
            
    except Exception as error:
        raise error
    
def registerTrack(idTraccia, titolo, autore, artisti, idAlbum, durata, fileName):

    try:
        query = "INSERT INTO traccia VALUES (%s, %s, %s, %s, %s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, (idTraccia, titolo, autore, artisti, idAlbum, durata, fileName, ))
    except Exception as error:
        raise error

def isArtistRegistred(id):

    try:
        query = "SELECT id FROM artista WHERE id=%s"
        with connection.cursor() as cursor:
            cursor.execute(query, (id, ))
            result = cursor.fetchone()

            print("[result of isArtistRegistred] ", result)

            if result:
                return True
            else:
                return False
            
    except Exception as error:
        raise error
        
def registerArtist(id, country, artist_name, descrizione):
    
    try:
        query = "INSERT INTO artista VALUES (%s, %s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, (id, country, artist_name, None, ))
    except Exception as error:
        raise error

def isAlbumRegistred(albumID):
    try:
        query = "SELECT id FROM album WHERE id=%s"
        with connection.cursor() as cursor:
            cursor.execute(query, (albumID, ))
            result = cursor.fetchone()

            if result:
                return True
            else:
                return False
            
    except Exception as error:
        raise error

def registerAlbum(id, nome, data):
    try:

        # Trasforma `data` in un oggetto datetime.date, se non lo è già
        # if isinstance(data, str):
        #     data = datetime.strptime(data, '%Y-%m-%d').date()
        # elif isinstance(data, datetime):
        #     data = data.date()  # Se `data` è datetime, prendiamo solo la parte di data

        query = "INSERT INTO album VALUES (%s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, (id, nome, data, ))
    except Exception as error:
        raise error

def isAlbum_ArtistRegistred(artistID, AlbumID):
    try:
        query = "SELECT * FROM artista_album WHERE artista_id=%s AND album_id=%s"
        with connection.cursor() as cursor:
            cursor.execute(query, (artistID, AlbumID, ))
            result = cursor.fetchone()

            if result:
                return True
            else:
                return False
            
    except Exception as error:
        raise error

def registerArtistAlbum(artistaID, albumID, owner):
    
    try:

        # Assicura che `owner` sia un booleano
        if not isinstance(owner, bool):
            raise ValueError("Il parametro 'owner' deve essere di tipo booleano.")
        
        query = "INSERT INTO artista_album VALUES (%s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, (artistaID, albumID, owner, ))
    except Exception as error:
        raise error

def getArtists():

    try:
        query = "SELECT * FROM artista"
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    except Exception as error:
        raise error

def getArtist(id: str):

    try:
        query = "SELECT * FROM artista WHERE id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, (id, ))
            return cursor.fetchall()

    except Exception as error:
        raise error

def getAlbums():

    try:
        query = "SELECT * FROM album"
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    except Exception as error:
        raise error
    
def getTracks():

    try:
        query = "SELECT * FROM traccia"
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    except Exception as error:
        raise error

def getTracksArtist(idArtist: str):

    try:
        query = "\
            SELECT * FROM traccia  \
            WHERE album_id IN \
            ( \
	            SELECT album_id FROM artista_album\
	            WHERE artista_id = %s\
            )"
        
        with connection.cursor() as cursor:
            cursor.execute(query, (idArtist))
            return cursor.fetchall()

    except Exception as error:
        raise error

# def fetchall_nameActress():
#     query="SELECT name FROM gallery_actress"

#     with connection.cursor() as cursor:
#         cursor.execute(query)
#         result = cursor.fetchall() #tuple di attributi del select ((name, ), ...)

#     result = [r[0] for r in result]
#     return result

# def fetchall_tag():
#     query="SELECT name FROM gallery_tag"

#     with connection.cursor() as cursor:
#         cursor.execute(query)
#         result = cursor.fetchall() #tuple di attributi del select ((name, ), ...)

#     result = [r[0] for r in result]
#     return result

# def fetch_video_duration(file):
#     query="SELECT duration FROM gallery_video WHERE name = %s"

#     with connection.cursor() as cursor:
#         cursor.execute(query, (file, ))
#         result = cursor.fetchall()

#     result = [r[0] for r in result]
#     return result
    

# def check_actress(name):
#     query = "SELECT name FROM gallery_actress WHERE name=%s"
#     with connection.cursor() as cursor:
#         cursor.execute(query, (name, ))
#         result = cursor.fetchone()

#         if result:
#             return True
#         else:
#             return False

# def insert_gallery_video(video, source, duration):
#     query="INSERT INTO gallery_video VALUES (%s, %s, %s)"
#     with connection.cursor() as cursor:
#         cursor.execute(query, (video, source,duration, ))

# def insert_actressVideo(video, actress):
#     query = "INSERT INTO gallery_video_actress (video_id, actress_id) VALUES (%s, %s)"
#     with connection.cursor() as cursor:
#         cursor.execute(query, (video, actress, ))

# def insert_newActress(name, thumb):

#     query = "INSERT INTO gallery_actress VALUES (%s, %s)"
#     with connection.cursor() as cursor:
#         cursor.execute(query, (name, thumb, ))