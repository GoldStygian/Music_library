import requests
import re
import logging

logger = logging.getLogger(__name__)

cache = {} # mb_artist_id : data

def last_fm_api(last_fm_api_key, mb_artist_id):

    if mb_artist_id in cache:
        data = cache[mb_artist_id]
        logger.debug(f"LAST FM API get data of {mb_artist_id} from cache")

    else:

        url = f"https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&mbid={mb_artist_id}&api_key={last_fm_api_key}&format=json"
        response = requests.get(url)
        data = response.json()
        
        cache[mb_artist_id] = data

        logger.debug(f"LAST FM API get data of {mb_artist_id} from request")

    return data

def get_artist_image_from_lastfm(mb_artist_id, last_fm_api_key):
    
    logger.debug(f"LAST FM API Fetching artist image for {mb_artist_id}")

    data = last_fm_api(last_fm_api_key, mb_artist_id)
    
    # Controlla per immagini diverse
    image_url = None
    for image in data.get("artist", {}).get("image", []):
        if image["size"] == "extralarge" and "default" not in image["#text"]:
            image_url = image["#text"]
            break
    return image_url

def get_artist_description_from_lastfm(mb_artist_id, last_fm_api_key):

    logger.debug(f"LAST FM API Fetching artist description for {mb_artist_id}")
    
    data = last_fm_api(last_fm_api_key, mb_artist_id)

    try:    

        text = data["artist"]["bio"]["content"] #descrizione estesa
        # text = data["artist"]["bio"]["summary"] #descrizione breve

        # Rimuove tutto ciò che si trova tra <a ...> e </a>
        text = re.sub(r'<a[^>]*>.*?</a>', '', text, flags=re.IGNORECASE)

        # Ripulisce spazi extra generati dalla rimozione
        text = re.sub(r'\s{2,}', ' ', text).strip()
        
        return text
    
    except KeyError as e:
        print ("[d] ", e)
        return None

# https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&mbid=197b70c7-8910-4030-ad03-632d82aa40e3&api_key=d282cc058961d8b9cf3751fb9aad6707&format=json

# {
#    "artist":{
#       "name":"Sia",
#       "mbid":"2f548675-008d-4332-876c-108b0c7ab9c5",
#       "url":"https://www.last.fm/music/Sia",
#       "image":[
#          {
#             "#text":"https://lastfm.freetls.fastly.net/i/u/34s/2a96cbd8b46e442fc41c2b86b821562f.png",
#             "size":"small"
#          },
#          {
#             "#text":"https://lastfm.freetls.fastly.net/i/u/64s/2a96cbd8b46e442fc41c2b86b821562f.png",
#             "size":"medium"
#          },
#          {
#             "#text":"https://lastfm.freetls.fastly.net/i/u/174s/2a96cbd8b46e442fc41c2b86b821562f.png",
#             "size":"large"
#          },
#          {
#             "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#             "size":"extralarge"
#          },
#          {
#             "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#             "size":"mega"
#          },
#          {
#             "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#             "size":""
#          }
#       ],
#       "streamable":"0",
#       "ontour":"1",
#       "stats":{
#          "listeners":"3699555",
#          "playcount":"136510951"
#       },
#       "similar":{
#          "artist":[
#             {
#                "name":"Adele",
#                "url":"https://www.last.fm/music/Adele",
#                "image":[
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/34s/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"small"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/64s/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"medium"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/174s/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"large"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"extralarge"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"mega"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":""
#                   }
#                ]
#             },
#             {
#                "name":"Paloma Faith",
#                "url":"https://www.last.fm/music/Paloma+Faith",
#                "image":[
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/34s/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"small"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/64s/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"medium"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/174s/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"large"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"extralarge"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"mega"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":""
#                   }
#                ]
#             },
#             {
#                "name":"Birdy",
#                "url":"https://www.last.fm/music/Birdy",
#                "image":[
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/34s/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"small"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/64s/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"medium"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/174s/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"large"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"extralarge"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"mega"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":""
#                   }
#                ]
#             },
#             {
#                "name":"Jessie J",
#                "url":"https://www.last.fm/music/Jessie+J",
#                "image":[
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/34s/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"small"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/64s/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"medium"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/174s/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"large"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"extralarge"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"mega"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":""
#                   }
#                ]
#             },
#             {
#                "name":"P!nk",
#                "url":"https://www.last.fm/music/P%21nk",
#                "image":[
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/34s/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"small"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/64s/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"medium"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/174s/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"large"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"extralarge"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":"mega"
#                   },
#                   {
#                      "#text":"https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
#                      "size":""
#                   }
#                ]
#             }
#          ]
#       },
#       "tags":{
#          "tag":[
#             {
#                "name":"female vocalists",
#                "url":"https://www.last.fm/tag/female+vocalists"
#             },
#             {
#                "name":"chillout",
#                "url":"https://www.last.fm/tag/chillout"
#             },
#             {
#                "name":"indie",
#                "url":"https://www.last.fm/tag/indie"
#             },
#             {
#                "name":"trip-hop",
#                "url":"https://www.last.fm/tag/trip-hop"
#             },
#             {
#                "name":"downtempo",
#                "url":"https://www.last.fm/tag/downtempo"
#             }
#          ]
#       },
#       "bio":{
#          "links":{
#             "link":{
#                "#text":"",
#                "rel":"original",
#                "href":"https://last.fm/music/Sia/+wiki"
#             }
#          },
#          "published":"12 Feb 2006, 14:27",
#          "summary":"Sia Kate Isobelle Furler (/ˈsiːə/; born 18 December 1975) is an Australian singer-songwriter, record producer and music video director. She started her career as a singer in the local Adelaide acid jazz band Crisp in the mid-1990s. In 1997, when Crisp disbanded, she released her debut studio album titled OnlySee in Australia. She then moved to London, England, and provided lead vocals for the British duo Zero 7.\n\nIn 2000, Sia signed to Sony Music's sub-label Dance Pool and released her second studio album \u003Ca href=\"https://www.last.fm/music/Sia\"\u003ERead more on Last.fm\u003C/a\u003E",
#          "content":"Sia Kate Isobelle Furler (/ˈsiːə/; born 18 December 1975) is an Australian singer-songwriter, record producer and music video director. She started her career as a singer in the local Adelaide acid jazz band Crisp in the mid-1990s. In 1997, when Crisp disbanded, she released her debut studio album titled OnlySee in Australia. She then moved to London, England, and provided lead vocals for the British duo Zero 7.\n\nIn 2000, Sia signed to Sony Music's sub-label Dance Pool and released her second studio album, Healing Is Difficult, the following year. Displeased with the promotion of the record, she signed to Go! Beat and released her third studio album, Colour the Small One, in 2004. The project struggled to connect with a mainstream audience, and so Sia relocated to New York City in 2005 and began touring across the United States. She released her fourth and fifth studio releases, Some People Have Real Problems and We Are Born, in 2008 and 2010, respectively. She then took a hiatus from performing, during which she focused on songwriting for other artists. Her catalogue includes the successful collaborations \"Titanium\" (with David Guetta), \"Diamonds\" (with Rihanna) and \"Wild Ones\" (with Flo Rida).\n\nIn 2014, Sia released her sixth studio album 1000 Forms of Fear, which debuted at No 1 in the U.S. Billboard 200 and generated the top-ten breakthrough single \"Chandelier\" and a trilogy of music videos starring child dancer Maddie Ziegler. In 2016, she released her seventh studio album This Is Acting, which spawned her first Hot 100 number one single, \"Cheap Thrills\". The same year, Sia gave her Nostalgic for the Present Tour, which incorporated performance art elements. Sia has received an array of accolades, including ARIA Awards and an MTV Video Music Award. \u003Ca href=\"https://www.last.fm/music/Sia\"\u003ERead more on Last.fm\u003C/a\u003E. User-contributed text is available under the Creative Commons By-SA License; additional terms may apply."
#       }
#    }
# }