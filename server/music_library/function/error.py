class CustomError(Exception):
    pass

class TrackJustRegistred(CustomError):
    pass

class NoAlbumImgFound(CustomError):
    pass

class NoArtistImgFound(CustomError):
    pass
