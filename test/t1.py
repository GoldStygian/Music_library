import requests
import json

headers = {
    'User-Agent': 'MyMusicApp/1.0 (contact@example.com)'
}

url = 'https://musicbrainz.org/ws/2/recording/cf7caec1-880b-4256-990f-430d47d3c154?inc=artist-credits+annotation&fmt=json'

response = requests.get(url, headers=headers)

# Safely print the JSON content
print(json.dumps(response.json(), ensure_ascii=False, indent=2))
