import requests

def get_artist_image_from_deezer(artist_name):
    url = f"https://api.deezer.com/search/artist?q={artist_name}"
    response = requests.get(url)
    data = response.json()
    
    if data["data"]:
        return data["data"][0]["picture_xl"]  # Immagine in alta risoluzione
    return None