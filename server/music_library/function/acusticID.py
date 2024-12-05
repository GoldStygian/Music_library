import requests

fingerprint = "12d5a2aa-33b2-47f8-ad54-220e9b3b755a"  # Inserisci qui il fingerprint generato da fpcalc
url = f"https://api.acousticbrainz.org/v1/lookup?fingerprint={fingerprint}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Errore nella ricerca.")
