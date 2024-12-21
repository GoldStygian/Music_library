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
    
def getVariantNum(idTrack):

    try:
        query = "SELECT variant FROM traccia WHERE id=%s"
        with connection.cursor() as cursor:
            cursor.execute(query, (idTrack, ))
            return cursor.fetchone()[0]
            
    except Exception as error:
        raise error

def registerTrack(idTraccia, titolo, autore, artisti, idAlbum, durata, fileName, variant):

    try:
        query = "INSERT INTO traccia VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, (idTraccia, titolo, autore, artisti, idAlbum, durata, fileName, variant, ))
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
            cursor.execute(query, (id, country, artist_name, descrizione, ))
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
            result = cursor.fetchone()
        
        result = {
            'id': result[0],
            'country': result[1],
            'name': result[2],
            'descrizione': result[3]
        }

        return result

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
	            WHERE artista_id = %s AND proprietario = true\
            )"
        
        with connection.cursor() as cursor:
            cursor.execute(query, (idArtist, ))
            result =  cursor.fetchall()
        
        result = [
        {
            'id': row[0],
            'titolo': row[1],
            'autore': row[2],
            'artistParticipants': row[3],
            'album_id': row[4],
            'durata': row[5],
            'fileName': row[6]
        }
        for row in result
        ]

        return result

    except Exception as error:
        raise error
    
def getAllTracksArtist(idArtist: str):

    try:
        query = "\
            SELECT * FROM traccia  \
            WHERE album_id IN \
            ( \
	            SELECT album_id FROM artista_album\
	            WHERE artista_id = %s\
            )"
        
        with connection.cursor() as cursor:
            cursor.execute(query, (idArtist, ))
            return cursor.fetchall()

    except Exception as error:
        raise error

def getAllData(idArtist: str):

    try:
        query = """
            SELECT 
                AA.album_id AS album_id,
                A.nome AS album_nome,
                A.data AS data_pubblicazione,
                STRING_AGG(AA.artista_id::text || ',' || Ar.artist_name, ';') AS artista,
                AA.proprietario AS proprietario,
                T.id,
                T.titolo,
                T.autore,
                T.artisti_partecipanti,
                T.durata,
                T.file_name,
                T.variant
            FROM 
                album AS A
            JOIN 
                artista_album AS AA ON A.id = AA.album_id
            JOIN 
                traccia AS T ON A.id = T.album_id
            JOIN 
                artista AS Ar ON AA.artista_id = Ar.id
            WHERE 
                AA.artista_id = %s
            GROUP BY 
                AA.album_id, A.nome, A.data, AA.proprietario, T.id, T.titolo, T.autore, T.artisti_partecipanti, T.durata, T.file_name, T.variant
        """

        with connection.cursor() as cursor:
            cursor.execute(query, (idArtist, ))
            result = cursor.fetchall()

            return result

    except Exception as error:
        raise error
